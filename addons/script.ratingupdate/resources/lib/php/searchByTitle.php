<?php

/*-------------------------*/
/* Rating Update           */
/* by Max (m4x1m) Headroom */
/*-------------------------*/

header ("Content-type: text/xml");

require_once ("../imdb/imdb.class.php");
require_once ("../imdb/imdbsearch.class.php");
$IMDb = new imdbsearch();
$IMDb->setsearchname($_GET["Title"]);
$Query = $IMDb->results();

if ($Query) {
echo <<<EOF
<?xml version="1.0" encoding="UTF-8" ?>
<root>
 <results>

EOF;
foreach ($Query as $Key=>$Value) {
     if (preg_match("/\b(TV Series|TV Movie|TV Mini)\b/", $Value->movietype())) {
echo <<<EOF
  <TVShows>
   <Title>{$Value->title()} ({$Value->year()})</Title>
   <ID>tt{$Value->imdbid()}</ID>
  </TVShows>

EOF;
     }
}
echo <<<EOF
 </results>
</root>

EOF;
}

?>
