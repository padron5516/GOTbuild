<?php

/*-------------------------*/
/* Rating Update           */
/* by Max (m4x1m) Headroom */
/*-------------------------*/

require_once ("../imdb/imdb.class.php");

if (isset($_GET["ID"])) {
     if (preg_match("/tt/", $_GET["ID"])) $ID = str_replace("tt", "", $_GET["ID"]); else $ID = $_GET["ID"];
     $Movie = new imdb($ID);
     if ($Movie) {
	  $MPAA = $Movie->mpaa(); if (isset($_GET["Country"])) $Country = $_GET["Country"]; else $Country = "USA";
	  echo '{"rating":"'.$Movie->rating().'","votes":"'.$Movie->votes().'","mpaa":"'.$MPAA[$Country].'","mpaa_reason":"'.$Movie->mpaa_reason().'","response":"true"}';
     } else echo '{"response":"false"}';
}

?>
