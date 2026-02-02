{% if message.sender == request.user %}
  <form method="post" action="{% url 'direct_message:delete_message' message.id %}" style="display:inline;">
    {% csrf_token %}
    <button type="submit" class="btn btn-sm btn-outline-danger">Delete</button>
  </form>
  <a href="{% url 'direct_message:edit_message' message.id %}" class="btn btn-sm btn-outline-secondary">Edit</a>
{% endif %}
