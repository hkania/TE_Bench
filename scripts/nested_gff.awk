BEGIN {
       	FS="\t"
        OFS="\t"
}


{print model"_artificial_sequence_"num, "GARLIC", $6, $2, $3, "100", $4, ".", $5";NA"}
