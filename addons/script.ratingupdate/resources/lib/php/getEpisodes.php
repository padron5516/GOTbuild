<?php

/*-------------------------*/
/* Rating Update           */
/* by Max (m4x1m) Headroom */
/*-------------------------*/

require_once ("../imdb/imdb.class.php");

if (isset($_GET["ID"])) {
     if (preg_match("/tt/", $_GET["ID"])) $ID = str_replace("tt", "", $_GET["ID"]); else $ID = $_GET["ID"];
     $tvShow = new imdb($ID);
     if ($tvShow) {
	  $jSon = '{"result":{"episodes":[';
	  foreach ($tvShow->episodes() as $Keys=>$Values) {
	       foreach ($Values as $Key=>$Value) { $jSon .= '{"season":"'.$Value['season'].'","episode":"'.$Value['episode'].'","imdbID":"tt'.$Value['imdbid'].'"},'; }
	  }
	  $jSon = rtrim($jSon, ",").']}}';
	  echo $jSon;
     } else echo '{"result":{"false":""}}';
}

?>
