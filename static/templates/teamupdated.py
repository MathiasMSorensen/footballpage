{% extends "base.html" %}
{% block title %}YEAH111{% endblock %}

{% block content %}
<!DOCTYPE html>
<html>
       <form action="/Adjustoptimization" method="POST">
 <table class="table table-striped">
  <thead>
    <tr>
      <th scope="col">#</th>
      <th scope="col">Name</th>
    </tr>
  </thead>
  
  <tbody>
      {% set count = namespace(value=1) %}
      {% for each in Squad %}
        <tr>
          <td> {{ count.value }} </td>
          <td> <input type="hidden" name="Name" value='{{ each }}'> {{ each }} </td>
          <td>{{ Squad_Position[count.value-1] }}</td>
            {% set count.value = count.value + 1 %}
      {% endfor %} 
         
    </tr>
  </tbody>
  </table>
  </html>
{% endblock %}
