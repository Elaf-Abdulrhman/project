from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Message
from django.db.models import Q, Max, Count
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

@login_required
def chat_page_view(request, username=None):
    if request.user.is_superuser:
        return redirect('admins:dashboard')

    search_query = request.GET.get('q', '')
    selected_user = None
    chat_messages = []
    unread_counts = {}

    if search_query:
    # If user is searching
        users = User.objects.filter(
            username__icontains=search_query,
            is_superuser=False
        ).exclude(id=request.user.id)

        if not users.exists():
            messages.info(request, "No users found matching your search.")
    else:
        # Get message queryset where current user is involved and has not deleted messages
        messages_qs = Message.objects.filter(
            Q(sender=request.user, sender_deleted=False) |
            Q(recipient=request.user, recipient_deleted=False)
        )

        # Track last interaction time with each user
        sent_times = messages_qs.filter(sender=request.user).values('recipient').annotate(last=Max('timestamp'))
        received_times = messages_qs.filter(recipient=request.user).values('sender').annotate(last=Max('timestamp'))

        last_message_map = {}
        for entry in sent_times:
            last_message_map[entry['recipient']] = entry['last']
        for entry in received_times:
            existing = last_message_map.get(entry['sender'])
            if not existing or entry['last'] > existing:
                last_message_map[entry['sender']] = entry['last']

        # Get unread message counts for badge display
        unread_counts_qs = (
            Message.objects
            .filter(recipient=request.user, is_read=False, recipient_deleted=False)
            .values('sender')
            .annotate(count=Count('id'))
        )
        unread_counts = {entry['sender']: entry['count'] for entry in unread_counts_qs}

        # Get user list sorted by last message timestamp
        user_ids = last_message_map.keys()
        users_qs = User.objects.filter(id__in=user_ids, is_superuser=False).exclude(id=request.user.id)
        users = sorted(users_qs, key=lambda u: last_message_map[u.id], reverse=True)

    # If user selected from chat list or URL
    if username:
        try:
            selected_user = User.objects.get(username=username)
            if selected_user.is_superuser or selected_user.id == request.user.id:
                selected_user = None
                messages.error(request, "You cannot chat with this user.")
            else:
                # Mark unread messages from selected_user as read
                Message.objects.filter(
                    sender=selected_user,
                    recipient=request.user,
                    is_read=False
                ).update(is_read=True)

                # Load conversation messages (respecting delete flags)
                chat_messages = Message.objects.filter(
                    Q(sender=request.user, recipient=selected_user, sender_deleted=False) |
                    Q(sender=selected_user, recipient=request.user, recipient_deleted=False)
                ).order_by('timestamp')
        except User.DoesNotExist:
            messages.error(request, f"No user found with username '{username}'.")

    # Handle sending message
    if request.method == 'POST' and selected_user:
        content = request.POST.get('content')
        if content:
            Message.objects.create(
                sender=request.user,
                recipient=selected_user,
                content=content
            )
            return redirect('direct_message:chat_page', username=selected_user.username)

    return render(request, 'direct_message/combined_chat.html', {
        'users': users,
        'selected_user': selected_user,
        'chat_messages': chat_messages,
        'search_query': search_query,
        'unread_counts': unread_counts,
    })

@login_required
def edit_message_view(request, message_id):
    message_obj = get_object_or_404(Message, id=message_id, sender=request.user)

    if request.method == 'POST':
        new_content = request.POST.get('content')
        if new_content:
            message_obj.content = new_content
            message_obj.save()
            return redirect('direct_message:chat_page', username=message_obj.recipient.username)
    
    return render(request, 'direct_message/edit_message.html', {'message': message_obj})

@login_required
def delete_message_for_me(request, message_id):
    message = get_object_or_404(Message, id=message_id, sender=request.user)
    message.sender_deleted = True
    message.save()
    return redirect('direct_message:chat_page', username=message.recipient.username)

@login_required
def delete_message_for_everyone(request, message_id):
    message = get_object_or_404(Message, id=message_id, sender=request.user)
    message.content = "This message was deleted"
    message.deleted_for_everyone = True
    message.save()
    return redirect("direct_message:chat_page", username=message.recipient.username)

@login_required
def clear_conversation(request, username):
    other_user = get_object_or_404(User, username=username)
    if request.method == 'POST':
        messages = Message.objects.filter(
            Q(sender=request.user, recipient=other_user) |
            Q(sender=other_user, recipient=request.user)
        )
        for m in messages:
            m.soft_delete(request.user)
        return redirect('direct_message:chat_page_view')
