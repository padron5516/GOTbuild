<?php

/*-------------------------*/
/* Rating Update           */
/* by Max (m4x1m) Headroom */
/*-------------------------*/

header ("Content-type: text/xml");

require_once ("../imdb/imdb.class.php");
require_once ("top250.Class.php");
$IMDb = new IMDbTop250;
$Query = $IMDb->GetTop250();

if ($Query) {
echo <<<EOF
<?xml version="1.0" encoding="UTF-8" ?>
<root>
 <results>

EOF;
foreach ($Query as $Key=>$Value) {
echo <<<EOF
  <Top250>
   <Title>{$Value['Title']}</Title>
   <ID>tt{$Value['ID']}</ID>
  </Top250>

EOF;
}
echo <<<EOF
 </results>
</root>

EOF;
}

?>