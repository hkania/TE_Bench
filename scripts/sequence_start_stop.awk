BEGIN {
	FS="\t"
	OFS="\t"
}

$3 == "100.000" {print $1, $9, $10}
