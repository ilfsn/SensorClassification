Set-ExecutionPolicy RemoteSigned

$SESSIONS_COUNT_LIMIT_MIN = 0
$SESSIONS_COUNT_LIMIT_MAX = 60000
$TRIMED_FILE_LEN = 784
$SOURCE_SESSION_DIR = "data"

echo "If Sessions more than $SESSIONS_COUNT_LIMIT_MAX we only select the largest $SESSIONS_COUNT_LIMIT_MAX."
echo "Finally Selected Sessions:"

$dirs = gci $SOURCE_SESSION_DIR -Directory
foreach($d in $dirs)
{
    $files = gci $d.FullName
    $count = $files.count
    if($count -gt $SESSIONS_COUNT_LIMIT_MIN)
    {             
        echo "$($d.Name) $count"        
        if($count -gt $SESSIONS_COUNT_LIMIT_MAX)
        {
            $files = $files | sort Length -Descending | select -First $SESSIONS_COUNT_LIMIT_MAX
            $count = $SESSIONS_COUNT_LIMIT_MAX
        }

        $files = $files | resolve-path
        $test  = $files | get-random -count ([int]($count/10))
        $train = $files | ?{$_ -notin $test}     

        $path_test  = "4_Png\Test\$($d.Name)"
        $path_train = "4_Png\Train\$($d.Name)"
        ni -Path $path_test -ItemType Directory -Force
        ni -Path $path_train -ItemType Directory -Force    

        cp $test -destination $path_test        
        cp $train -destination $path_train
    }
}