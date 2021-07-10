<html>
	<head>
		<title> {{report_title}} </title>
		<meta charset="utf-8">
		  <meta name="viewport" content="width=device-width, initial-scale=1">
		  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
		  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
		  <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
		  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
	</head>
	<style>
	
		.bg-custom-2 
		{
			background-image: linear-gradient(15deg, #13547a 0%, #80d0c7 100%);
		}
	</style>
	
	<body>
		<nav class="navbar navbar-dark bg-custom-2">
  			<a class="navbar-brand" href="#a">RazorPy</a>
		</nav>
		
		{% for exec_data in execution_details %}
		<div class="card">
		  <div class="card-header">
		    {{ exec_data.task }}
		  </div>
		  <div class="card-body">
		    {% if exec_data.status == "Success" %}
		    	<h5 class="card-title">Status: <span class="badge badge-success">{{ exec_data.status }}</span></h5>
		    {% elif exec_data.status == "Failure" %}
		    	<h5 class="card-title">Status: <span class="badge badge-danger">{{ exec_data.status }}</span></h5>
		    {% elif exec_data.status == "Skipped" %}
		    	<h5 class="card-title">Status: <span class="badge badge-warning">{{ exec_data.status }}</span></h5>
		    {% else %}
		    	<h5 class="card-title">Status: <span class="badge badge-dark">Unknown</span></h5>
		    {% endif %}
		    <p class="card-text font-weight-light"><b>Time taken to complete this task:</b> <mark>{{ exec_data.time }} seconds</mark></p>
		    <p class="card-text font-weight-light"><b>Output returned by this task:</b> <mark>{{ exec_data.output }}</mark></p>
		  </div>
		</div>
		{% endfor %}
		
	</body>
</html>