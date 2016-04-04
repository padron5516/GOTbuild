<?php

/*-------------------------*/
/* Rating Update           */
/* by Max (m4x1m) Headroom */
/*-------------------------*/

include_once ("../imdb/mdb_base.class.php");

class IMDbTop250 {

     var $Top250Url  = "http://www.imdb.com/chart/top";
     var $Top250Page = "";

     function IMDbTop250() {
	  $Query = new MDB_Request($this->Top250Url);
	  $Query->sendRequest();
	  $this->Top250Page = $Query->getResponseBody();
     }

     function GetTop250() {
	  $matchStart = "Showing 250 Titles";
	  $startPos = strpos($this->Top250Page, $matchStart);
	  $startPos += (strlen($matchStart) + 1);
	  $i = 0; $Result = "";
	  $offSet = $startPos;
	  while ($i < 250) {
	       $SectionsPattern = '/<td class="titleColumn">(.*?)\/td>/s';
	       $TitlesPattern   = '/" >(.*?)<\/a>/s';
	       $YearsPattern    = '/\((\d+)\)/';
	       $IMDbIDsPattern  = '/\/tt(\d+)\//s';
	       preg_match($SectionsPattern, $this->Top250Page, $matchSections, PREG_OFFSET_CAPTURE, $offSet);
	       preg_match($TitlesPattern, $matchSections[0][0], $matchTitle);
	       preg_match($YearsPattern, $matchSections[0][0], $matchYear);
	       preg_match($IMDbIDsPattern, $matchSections[0][0], $matchesIMDbID);
	       $Title = $matchTitle[1]." (".$matchYear[1].")";
	       $IMDbID = $matchesIMDbID[1];
	       $Result[$i] = array("ID" => $IMDbID, "Title" => $Title);
	       $offSet = $matchSections[0][1]+1;
	       $i++;
	  }
	  return $Result;
     }

}

?>
