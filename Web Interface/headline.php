<?php

if(isset($_POST)){
    
    if(isset($_POST['headline'])){
        $type = (int)$_POST['type'];
        $retval = 0;
        
        if($type == 1){
            $mystring = system("python hedge_trimmer.py summary.txt", $retval);
            if( $retval == 0 ){
                $headline = fopen("headline.txt", "r") or die("Unable to open file!");
                $text = mb_convert_encoding(fread($headline,filesize("headline.txt")),'auto');
                fclose($headline);
                echo $text;

            } else{
                echo "Error";
            }
        } else{
            $mystring = system("python taggerHG.py summary.txt", $retval);
            if( $retval == 0 ){
                $headline = fopen("headline.txt", "r") or die("Unable to open file!");
                $text = mb_convert_encoding(fread($headline,filesize("headline.txt")),'auto');
                fclose($headline);
                echo $text;

            } else{
                echo "Error";
            }
        }
        
    } elseif(isset($_POST['feedback'])){
        $type = (int)$_POST['type'];
        $headline = $_POST['head'];
        $headAlgo = $_POST['headAlgo'];
        $sumAlgo = $_POST['sumAlgo'];
        $comment = $_POST['comment'];
        
        $myfile = fopen("feedback.txt", "a") or die("Unable to open file!");
        $txt = "$type;$sumAlgo;$headAlgo;$headline;$comment".PHP_EOL;
        fwrite($myfile, $txt);
        fclose($myfile);
        echo $type;
        
    } elseif(isset($_POST['chart'])){
        $count1 = 0;
        $count2 = 0;
        $count3 = 0;
        $count4 = 0;
        $handle = fopen("feedback.txt", "r");
        if ($handle) {
            while (($line = fgets($handle)) !== false) {
                $words = explode(" ", $line);
                
                if((int)$words[0] == 1 ){
                    $count1 += 1;
                } elseif((int)$words[0] == 2 ){
                    $count2 += 1;
                } elseif((int)$words[0] == 3 ){
                    $count3 += 1;
                } elseif((int)$words[0] == 4 ){
                    $count4 += 1;
                } 
            }
            echo "$count1 $count2 $count3 $count4";

            fclose($handle);
        } else {
            // error opening the file.
        }
    
    }else{
        $article = $_POST['article'];
        $lines = $_POST['lines'];
        $type = (int)$_POST['type'];

        $article = mb_convert_encoding($article, "latin1");

        $myfile = fopen("article.txt", "w") or die("Unable to open file!");
        fwrite($myfile, $article);
        fclose($myfile);

        if( $type == 1){
            $mystring = system("python textRank.py article.txt $lines", $retval);
            if( $retval == 0 ){
                $summary = fopen("summary.txt", "r") or die("Unable to open file!");
                $text = mb_convert_encoding(fread($summary,filesize("summary.txt")),'auto');
                fclose($summary);
                echo $text;

            } else{
                echo "Error";
            }
        } else{
            $mystring = system("python LexRankSummarizer.py article.txt $lines", $retval);
            if( $retval == 0 ){
                $summary = fopen("summary.txt", "r") or die("Unable to open file!");
                $text = mb_convert_encoding(fread($summary,filesize("summary.txt")),'auto');
                fclose($summary);
                echo $text;

            } else{
                echo "Error";
            }
        }
    }
}
?>