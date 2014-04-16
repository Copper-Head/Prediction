compare = function(n1, n2, df){
  sents1 = subset(df, condition==n1, select=probability)
#   print(sents1)
  sents2 = subset(df, condition==n2, select=probability)
  difference = sents1 - sents2
  return(mean(difference[['probability']]))
}