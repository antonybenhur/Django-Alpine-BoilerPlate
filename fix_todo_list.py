content = """{% for todo in todos %}
<tr>
    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">{{ todo.title }}</td>
    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">{{ todo.description|truncatechars:50 }}</td>
    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">{{ todo.created_at|date:"Y-m-d H:i:s" }}</td>
    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
        {% if todo.is_completed %}
        <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200">Completed</span>
        {% else %}
        <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200">Pending</span>
        {% endif %}
    </td>
</tr>
{% empty %}
<tr>
    <td colspan="4" class="px-6 py-4 text-center text-sm text-gray-500 dark:text-gray-400">No ToDo items generated yet. Schedule the task to see them appear here!</td>
</tr>
{% endfor %}
"""

with open(r'c:\AntiGravity\DjangoBP\templates\demos\partials\todo_list.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("File written successfully")
