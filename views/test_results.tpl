<!DOCTYPE html>
<html>
<head>
<title>Harbor</title>
</head>
<body>
<p>
Test {{name}}
</p>
<ul>
<table border cellpadding=8>
<tr>
<th><b>Testname</th>
<th>Description</th>
<th>Result</th>
<th>Date</th>
<th>Error Message</b></th>
</tr>
%for items in testresults:
<tr>
%for item in items:
<td>
{{item}}
</td>
%end
</tr>
%end
</table>
</ul>
</body>
</html>
