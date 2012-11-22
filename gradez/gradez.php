<?php
// https://developers.google.com/gdata/samples/spreadsheet_sample

header('Content-type: application/json');
$feed = 'https://docs.google.com/spreadsheet/pub?hl=en_US&hl=en_US&key=0AqfP9C6R7wKrdGRYOGc1V000ZzJpdVRWLWN1dEl4ekE&single=true&gid=0&output=csv';
$keys = array();
$newArray = array();
 
// CSV -> associative array
function csvToArray($file, $delimiter) { 
  if (($handle = fopen($file, 'r')) !== FALSE) { 
    $i = 0; 
    while (($lineArray = fgetcsv($handle, 4000, $delimiter, '"')) !== FALSE) { 
      for ($j = 0; $j < count($lineArray); $j++) { 
        $arr[$i][$j] = $lineArray[$j]; 
      } 
      $i++; 
    } 
    fclose($handle); 
  } 
  return $arr; 
} 
 
$data = csvToArray($feed, ',');
$count = count($data) - 1; // first row is header
$labels = array_shift($data);  
foreach ($labels as $label) { $keys[] = $label; }

$keys[] = 'id';
for ($i = 0; $i < $count; $i++) { $data[$i][] = $i; }
 
for ($j = 0; $j < $count; $j++) {
  $d = array_combine($keys, $data[$j]);
  $newArray[$j] = $d;
}
 
echo json_encode($newArray);
 
?>

