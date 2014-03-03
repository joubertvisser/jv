<!DOCTYPE html>
<html>
<head>
<title>Hello World!</title>
</head>
<body>
<p>
Testing {{username}}
</p>
<ul>
%for thing in things:
<li>{{thing}}</li>
%end
</ul><p>
<form action="/favorite_fruit" method="POST">
What is your favorite test?
<input type="text" name="fruit" size="40" value=""><br>
</form>
</body>
</html>
