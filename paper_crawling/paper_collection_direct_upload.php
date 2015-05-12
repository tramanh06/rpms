<?php 
if($_SERVER['REQUEST_METHOD'] == "GET") {
  $user['email'] = $_GET["email"];
  $user['firstname'] = $_GET["firstname"];
  $user['lastname'] = $_GET["lastname"];
} elseif($_SERVER['REQUEST_METHOD'] == "POST") {
  $user['email'] = $_POST["email_django"];
  $user['firstname'] = $_POST["firstname"];
  $user['lastname'] = $_POST["lastname"];
}

?> 

<head>
<meta content='text/html; charset=UTF-8' http-equiv='Content-Type'>
<title> &ndash; File Manager <?php if(isset($user)) {echo $user['email']; } ?> </title>
<link rel='stylesheet' href='/webapp/fm/media/style.css' type='text/css'>
<link rel="stylesheet" type="text/css" href="/static/admin/css/base.css" />

<script type="text/javascript" src="/webapp/fm/media/jsi18n/"></script>
<script type="text/javascript" src="/webapp/fm/media/jquery.js"></script>
<script type="text/javascript" src="/webapp/fm/media/jquery.clipboard.js"></script>
<script type="text/javascript" src="/webapp/fm/media/jsi18n/"></script>

<script>
var pwd = "";
var url_media = "/webapp/fm/media";
var url_preview = "/webapp/fm/preview/";
var url_geturl = "/webapp/fm/geturl/";
var url_home = "/webapp/fm/list/";
var url_view = "/webapp/fm/view/";
var url_delete = "/webapp/fm/del/";
var url_destraction = "/webapp/fm/dest/";
</script>
<script type="text/javascript" src="/webapp/fm/media/script.js"></script>

</head>

<body>

</div>
<div id="main">

<?php

###################
#  Purpose    : 
#   - Interface for paper upload
#
#  Important variables --  
#  $dirPubs   : directory into which we create one file per user containing the
#               reviewer name and URLs
#  $dirPapers : directory into which we download papers
#  $dirBak    : backup directoy, move user directory there when a second upload occurs
#  $emailMaintainer : email to which problems should be sent to
#  $wget      : path to wget (older version had problems, version 1.12 is ok)
# 
#  Limitations -- 
#   - file that end in a / are assumed to be links to pdfs
#
# Author: Laurent Charlin, lcharlin@cs.toronto.edu
###################



ini_set('display_errors', 0);
ini_set('track_errors', '1');
@ini_set('user_agent', '"Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.8) Gecko/20100225 Iceweasel/3.5.8 (like Firefox/3.5.8)"');
ini_set('from', 'reviewer-paper-matching-problems@cs.toronto.edu');

$emailMaintainer = 'reviewer-paper-matching-problems@cs.toronto.edu';
$wget = '/usr/bin/wget'; # needs to be wget 1.12 or later, older wget have a bug. 
$rootdir = '../../reviewer_data/';
$dirPubs = $rootdir.'pubs/';
$dirBak =  $rootdir.'bak/';
$dirPapers = 'papers/';

function replace_chars($localFile) { 

 // only keep some allowed characters
  $allowed = "/[^\w\d\\040\\.\\-\\_\\(\\)]/i";
  return preg_replace($allowed,"",$localFile);

}


# Function which retrieves the files using CURL 
function get_file($localFile, $pub) { 
  $ctx = stream_context_create(array(
        'http' => array(
          'timeout' => 20
          )
        )
      ); 

  $indicator=1;

  $ch = curl_init();
  curl_setopt($ch, CURLOPT_URL,$pub); 
  curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
  curl_setopt($ch, CURLOPT_TIMEOUT, 200); // number of seconds after which it times out 
  curl_setopt($ch, CURLOPT_USERAGENT, "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.8) Gecko/20100225 Iceweasel/3.5.8 (like Firefox/3.5.8)");
  curl_setopt($ch, CURLOPT_FOLLOWLOCATION,  true);
  curl_setopt($ch, CURLOPT_MAXREDIRS,  10);
  curl_setopt($ch, CURLOPT_AUTOREFERER, true);

  if(preg_match("/^(ftp?:\/\/)/", $pub)) {  # for ftp use curl... 
    curl_setopt($ch, CURLOPT_FTP_USE_EPSV, 0); 
  }

  $localFile = urldecode($localFile); // remove url markup
  $localFile = dirname($localFile).'/'.replace_chars(basename($localFile));

  # if localFile already exists, change its name 
  $fileExisted = 0; 
  if(file_exists($localFile)) { 
    srand();
    $oldlocalFile = $localFile;
    $localFile = $localFile.rand(0, getrandmax());
    $fileExisted = 1; 
  }

  $fp = fopen($localFile, 'w'); 
  if($fp == FALSE) { 
    echo "Problem opening local file, please email reviewer-paper-matching-problems@cs.toronto.edu<br />";	
    echo $php_errormsg;
    $indicator =0;
    return $indicator; 
  } 

  curl_setopt($ch, CURLOPT_FILE, $fp);

  if(curl_exec($ch) == FALSE)  { 
    echo '<font color="red"><b> Could not retrieve file (1)</b></font><br />';
    echo 'Error: '.curl_error($ch)."<br />";
    $indicator=0; 
    curl_close($ch);
    return $indicator; 
  }
  fclose($fp); 
  curl_close($ch); 

  if($fileExisted==1) { # make sure that you don't keep copies of the same file
    exec('md5sum '.$localFile." |awk '{ print $1 }'", $out);
    exec('md5sum '.$oldlocalFile." |awk '{ print $1 }'", $out_old);
    if($out_old[0] == $out[0]){
      unlink($localFile);
    }
    else { echo '<br />files are different'.$out_old[0].' '.$out[0]; } 

  } 

  return $indicator; 

}


function flush_now() {

  @apache_setenv('no-gzip', 1);
  @ini_set('output_buffering', 0);
  @ini_set('zlib.output_compression', 0);
  @ini_set('implicit_flush', 1);
  for ($i = 0; $i < ob_get_level(); $i++) { ob_end_flush(); }
  ob_implicit_flush(1);
  return true;

}

function flush_buffers() {
  ob_end_flush();
  ob_flush();
  flush();
  ob_start();
} 


# from http://www.addedbytes.com/code/email-address-validation/
function check_email_address($email) { // First, we check that there's one @ symbol, and that the lengths are right 
  if (!ereg("^[^@]{1,64}@[^@]{1,255}$", $email)) { // Email invalid because wrong number of characters in one section, or wrong number of @ symbols. 
    return false; 
  } 

  // Split it into sections to make life easier 
  $email_array = explode("@", $email); $local_array = explode(".", $email_array[0]); 
  for ($i = 0; $i < sizeof($local_array); $i++) { 
    if (!ereg("^(([A-Za-z0-9!#$%&'*+/=?^_`{|}~-][A-Za-z0-9!#$%&'*+/=?^_`{|}~\.-]{0,63})|(\"[^(\\|\")]{0,62}\"))$", $local_array[$i])) { 
      return false; 
    } 
  } 
  if (!ereg("^\[?[0-9\.]+\]?$", $email_array[1])) { // Check if domain is IP. If not, it should be valid domain name 
    $domain_array = explode(".", $email_array[1]); 
    if (sizeof($domain_array) < 2) { 
      return false; // Not enough parts to domain 
    } 
    for ($i = 0; $i < sizeof($domain_array); $i++) { 
      if (!ereg("^(([A-Za-z0-9][A-Za-z0-9-]{0,61}[A-Za-z0-9])|([A-Za-z0-9]+))$", $domain_array[$i])) { 
        return false; 
      } 
    } 
  } return true; 
}

function removeDir($dir) { # remove dir and all its content
  system('rm -rf '.escapeshellarg($dir));
}

function ensureDirExists($dir, $bakDir) { 
  if(!file_exists($dir)) { 
    if(!mkdir($dir)) { 
      return False;
    } 
  }
  return True;
}


# Retrieve papers
function get_papers($pubs, $outDir, $dirBak, $wget) { 

  if(!ensureDirExists($outDir, $dirBak)) {  
    echo 'Could not create output dir<br />';
    echo $outDir.'<br />'; 
    echo $dirBak; 
    return False;
  }

  $pubs = preg_split("/((\r(?!\n))|((?<!\r)\n)|(\r\n)|( ))/", $pubs, null, PREG_SPLIT_NO_EMPTY);

  $indicator = 1;
  echo "Retrieving...<br/>\r\n";
  echo '<ol>';
  flush_now();
  foreach($pubs as $pub) { 

    # 1) Add http to link 
    if(!preg_match("/^(https?:\/\/)/", $pub) and !preg_match("/^(ftp?:\/\/)/", $pub)) {
      $pub = "http://".$pub;	
    }
    echo '<li />'.$pub.' -- ';
    flush_now();

    # 1.5) Check that it's a good link
    if(!filter_var($pub, FILTER_VALIDATE_URL, FILTER_FLAG_SCHEME_REQUIRED)) {
      echo '<font color="red"><b>  Cannot parse this URL: Invalid URL</b></font><br />';
      $indicator=0;
      continue;

    } elseif (preg_match("/\.pdf$/", $pub)) {  # PDF FILE: download it directly 

      $localFile = $outDir.'/'.basename($pub);
      echo "Single PDF download<br />";
      $ind = get_file($localFile, $pub); 
      if ($ind == 0) {
        continue; 
        $indicator=$ind;
      }
      echo '<font color="green"><b> Single PDF - Retrieved.</b></font><br />';
    } 
    else { # HTML FILE containing pdfs: download all pdfs linked from it
          # Call wget -r to _list_ the pdfs on that page. Parse that list to
          # retrieve the pdf filenames. Then retrieve all pdfs using php
          # functions (curl). This is a little convoluted but gives us a bit
          # more control (e.g., with error messages). 
      $useragent='"Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.8) Gecko/20100225 Iceweasel/3.5.8 (like Firefox/3.5.8)"';
      unset($files);
      #exec("cd ".escapeshellarg($outDir).";".$wget." -U ".$useragent." --timeout=15 -t 1 -r --spider --level=1 -H -nd -nc -A pdf ".escapeshellarg($pub)." 2>&1 | tee -a /tmp/toto3");
      date_default_timezone_set("America/Toronto");
      $outDirSafe = escapeshellarg($outDir); 
      $tmpDir = "tmp_".rand(0, getrandmax()); 
      $command = "cd ".$outDirSafe;
      $command = $command."; mkdir ".$tmpDir.";mv * ".$tmpDir.";";
      $command = $command.$wget." -U ".$useragent." --no-use-server-timestamps --timeout=15 -t 2 -r --spider --level=1 -H -nd -nc -A pdf -e robots=off ".escapeshellarg($pub)." 2>&1 | grep '\.pdf' | grep '^--". date("Y")."' | awk -F'  ' '{ print $(NF) }'";
      $command = $command."mv ".$tmpDir."/* .;";
      $command = $command."rmdir ".$tmpDir.";";
      #echo $command;
      exec($command, $files, $ret); 
      if($ret==0)
        echo 'Ok ('.count($files).' links)<br />';
      else { 
        echo '<font color="red"><b> Could not retrieve file (2)</b></font><br />';
        $indicator=0;
        continue; 
      }

      echo '<ul>';
      # maybe it's a single pdf (e.g., arxiv.org does this)
      if (count($files) == 0) { 
        echo '<li /> Did not find any PDFs at: '.$pub.' '; 
        $localFile = $outDir.'/'.basename($pub).'.pdf';
        get_file($localFile, $pub); 
        if (strcmp(finfo_file($fhandle,$_FILES["file"]["tmp_name"]), "application/pdf") == 0) { 
          echo '<font color="green"><b> Single PDF - Retrieved.</b></font><br />';
        } else { # downloaded file is not a PDF
          echo '<br /><font color="red"><b> File is a not a pdf file, discarding.</b></font><br />'; 
          unlink($localFile); 
        } 
      }

      # retrieve files 
      foreach($files as $file) { 
        if(strlen($file) == 0)
          continue; 
        echo '<li />'.$file.' '; 
        $localFile = $outDir.'/'.basename($file);
        $ind = get_file($localFile,  $file); 
        if ($ind == 0) {
          continue; 
          $indicator = $ind; 
        }
        echo '<font color="green"><b> PDF - Retrieved.</b></font><br />';
      }
      echo '</ul>';

    }
  } 
  echo '</ol>';

  return $indicator;

}

# MAIN 
if($_SERVER['REQUEST_METHOD'] == "POST") { # Do something if the form was submitted

  // code from: http://andrewcurioso.com/2010/06/detecting-file-size-overflow-in-php/
  if ( empty($_POST) && empty($_FILES) )
  {       
    $displayMaxSize = ini_get('post_max_size');

    switch ( substr($displayMaxSize,-1) )
    {
      case 'G':
        $displayMaxSize = $displayMaxSize * 1024;
      case 'M':
        $displayMaxSize = $displayMaxSize * 1024;
      case 'K':
        $displayMaxSize = $displayMaxSize * 1024;
    }
    $error = 'The file you tried uploading is too large. The maximum size is '.  $displayMaxSize.' bytes.';

    echo '<br /><font color="red" />' . $error . '<font color="black" />'; 

  } else { 

    if (!isset($_POST["direct_upload"])) { 
      $user['email'] = $_POST["email"];
      $user['firstname'] = $_POST["firstname"];
      $user['lastname'] = $_POST["lastname"];
      $user['publications'] = $_POST["publications"];
    } 
    else { // 
      $user['email'] = $_POST["email"];
    }

    $length['email'] = 250;
    $length['firstname'] = 250;
    $length['lastname'] = 250;
    $length['publications'] = 500000;
    $name['email'] = 'email address';
    $name['firstname'] = 'First Name';
    $name['lastname'] = 'Last Name';
    $name['publications'] = 'Publications';

    # Make sure that variables are safe
    $stop = 0; 
    if(!check_email_address($user['email'])) {
      $err[] =  "Your ". $name['email'] ." doesn't appear to be a valid email address.";
      $stop = 1;
    }

    if (isset($_POST["direct_upload"])) { 

      $uploaddir = $dirPubs.$dirPapers.$user['email'].'/'; 
      $fhandle = finfo_open(FILEINFO_MIME_TYPE); #($finfo, $_FILES["file"]["tmp_name"])
        if (isset($user) && strlen($user['email']) != 0)  { 
          if (strcmp(finfo_file($fhandle,$_FILES["file"]["tmp_name"]), "application/pdf") == 0)
            // Below it checks what the user's browser said while above it
            // checks the first couple bytes of the file. Hence, above is
            // more robust and harder to temper
            //if ($_FILES["file"]["type"] == "application/pdf" || $_FILES["file"]["type"] == "application/nappdf" || $_FILES["file"]["type"] == "application/force-download") 
            // && ($_FILES["file"]["size"] < 20000))
          {
            if ($_FILES["file"]["error"] > 0)
            {
              echo "Return Code: " . $_FILES["file"]["error"] . "<br />";
            }
            else
            {
            #echo "Upload: " . $_FILES["file"]["name"] . "<br />";
            #echo "Type: " . $_FILES["file"]["type"] . "<br />";
            #echo "Size: " . ($_FILES["file"]["size"] / 1024) . " Kb<br />";
            #echo "Temp file: " . $_FILES["file"]["tmp_name"] . "<br />";
            #$mime_type = $file_info->buffer(file_get_contents($_FILES["file"]["tmp_name"])); 
            #echo "mime_type " . $mime_type . "<br />";
            #if(strcmp($mime_type, "application/pdf") == 0) 
            #    echo "IS PDF<br />"; 

              $localFile = $_FILES["file"]["name"];
              $localFile = escapeshellarg($localFile);
              $localFile = replace_chars($localFile);

              if (file_exists($uploaddir . $localFile))
              {
                echo '<br /><font color="red"/>' . $localFile . ' already exists. <font color="black" />';
              }
              else
              {
                if (!move_uploaded_file($_FILES["file"]["tmp_name"], $uploaddir . $localFile)) {
                  echo "Could not save file</br>" .  $localFile; 
                }
                else { 
                  echo '<font color="green">Successfully saved: ' .  $localFile . '<font color="black">';
                } 
              }
            }
          } else {
            #$finfo = finfo_open(FILEINFO_MIME_TYPE);
            echo  finfo_file($fhandle, $_FILES["file"]["tmp_name"]).'<br />'; 
            echo "File does seem to be a valid pdf file: file type should be application/pdf and '".$_FILES["file"]["type"]."' found."; 
          }
        } else { 
          echo '<font color="red"/>Unknown user email: make sure that you are logged in to the system<font color="black"/>'; 
        }

    } else { 

      foreach($user as $key => $value) {
        if(empty($value)) { # empty vars
          $err[] =  $name[$key] . " entry is empty" . $email;
          $stop = 1; 
        }
        if(strlen($value) > $length[$key]) { # excessive size vars
          $err[] =  $name[$key] . " entry is too long (max allowed value is " . $length[$key] .')';
          $stop = 1;
        }
      }

      if(!$stop) { # Save file 
        $fileName = $dirPubs.$user['email'];

        if(!touch($fileName) or !chmod($fileName, 0600)) {
          echo "Your informations could not be saved. Something has gone horribly wrong in the filesystem... Please email ". $emailMaintainer;
          return;
        }

        $fp = fopen($fileName, 'w'); 
        fwrite($fp, $user['firstname'].' // ');
        fwrite($fp, $user['lastname']."\n");
        fwrite($fp, $user['publications']); 
        fclose($fp);
        chmod($fileName, 0640);

        if(get_papers($user['publications'], $dirPubs.$dirPapers.$user['email'], $dirBak, $wget))
          echo '<font color="blue"/><h1>Please check the above log to insure that all papers from your list have been successfully retrieved.<br /><font color="black"/> If so, you are done, thanks for your help!<font color="black"/><br/> If you have made a mistake you may resubmit your information.</h1><h3>For bug reports please contact: reviewer-paper-matching-problems@cs.toronto.edu</h3><p/>';
        else 
          echo '<font color="red"/><h1>We were unable to retrieve at least one of your links. You may want to resubmit your information<font color="black"/></h1><p/>';

      } else { # list errors
        echo '<font color="red"/><ul>';
        foreach($err as $value) {
          echo '<li/>'. $value;
        }
        echo '<ul/><font color="black"/><p/>';
      }

    }


  } // if _POST not empty 

} // if POST



?> 


<!-- HTML FORM --> 
<br />
<h4>Please use either (or both) of the following options to populate
your paper profile. <br />If possible please provide at least 5-10 publications.</h4>
<form method="POST" action="paper_collection_direct_upload.php"> 
<p />
<table border="0">
<input type="hidden" name="email" value="<?php if(isset($user)) { echo $user['email'];}?>" size="40"/>
<input type="hidden" name="firstname" value="<?php if(isset($user)) {echo $user['firstname'];} ?>" size="40"/>
<input type="hidden" name="lastname" value="<?php if(isset($user)) {echo $user['lastname'];}?>" size="40"/>
<p />
<br />
<h2>1) Papers from URLs</h2>
Representative publications, <b>one per line in either (or both)</b> of the following formats:
<ul> 
<li /> Paper URL (e.g. http://www.foo.edu/bar.pdf)
<li /> The URL of a publications page (all pdf papers that can be directly retrieved from that page will be used)
  </ul>


  <textarea cols="80" rows="15" name="publications" wrap="off" ><?php if(isset($user) && isset($user['publications']))  {echo $user['publications'];} ?></textarea>
  <p />
  <table width="100%">
  <tr><td width="75%">
  Once you press "Download papers" we will start downloading your papers. <br/>This operation
  might take a few minutes. During this time we will try to keep you updated on
  the progress of the downloads.<br/>
  </td><td>
  <tr><td>
  <input type="submit" value="Download papers" /><p/>
  <input type="hidden" name="email_django" value="<?php echo $user['email'] ?>" /> 
  </td><td>
  <br/>
  <input type="reset" /> 
  </td></tr>
  </table>

  </form> 
  <hr /><hr /> 

  <h2>2) Papers from your hard drive</h2>
  <form id="file_upload_form" method="post" enctype="multipart/form-data" action="paper_collection_direct_upload.php">
  <input name="file" id="file" size="27" type="file" /><br />
  <input type="submit" name="action" value="Upload" /><br />
  <input type="hidden" name="direct_upload" value="1" /> 
  <input type="hidden" name="email" value="<?php echo $user['email'] ?>" /> 
  <input type="hidden" name="firstname" value="<?php echo $user['firstname'] ?>" /> 
  <input type="hidden" name="lastname" value="<?php echo $user['lastname'] ?>" /> 
  <input type="hidden" name="email_django" value="<?php echo $user['email'] ?>" /> 
  </form>


  <h5>To report problems please contact: <?php echo $emailMaintainer ?></h5>
  </div>
  </body>
  </html>
