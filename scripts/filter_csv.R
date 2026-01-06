# this script filters an input csv by a specified target value and saves
# it as a new csv

###USER INPUT REQUIRED####################################################
# gather input
input_csv <- snakemake@input[['csv']] # path to input csv

output_csv <- snakemake@output[['csv']] # path to output csv

column <- snakemake@params[['column']] # column in input_csv containing target value

target <- snakemake@wildcards[['type']] # target value in column

##########################################################################

print(target)
print(column)
# load libraries
library(dplyr)
library(tidyr)

column <- as.numeric(gsub("^V", "", column))
df <- read.csv(input_csv, header = FALSE)

filtered_df <- df[df[[column]] == target, ]

# save filtered data frame as output_csv
write.table(filtered_df, file = output_csv, row.names = FALSE, col.names = FALSE, sep=",")
