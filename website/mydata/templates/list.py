
<!DOCTYPE html>
<html lang="en">
<head>
  <title>GLOSA Database</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js"></script>
</head>
<body>
<div class="container">
  <h2>Worst Bus Delays</h2>
  <p>The table below shows the worst delay periods on the monitored bus routes over the past 8 weeks.</p>            
  <table class="table table-striped table-dark table-sm">
    <thead>
      <tr>
        <th>Name</th>
        <th>Number</th>
      </tr>
    </thead>
    <tbody>
{% for post in posts%}
  <tr><td><{{post[0]}}<td>{{post[1]}}
{% endfor %}
</tbody>
</table>
</div>
</body>
</html>
