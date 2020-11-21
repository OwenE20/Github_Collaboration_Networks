

library(tidyverse)


facebook <- read.csv("Facebook_final.csv")


#Stats about facebook contributors
#summary(facebook$contributions)

#hist(facebook$contributions)
#boxplot(facebook$contributions)

#What if we filter out people with only the median contribution?
top_50 <- facebook %>% filter(facebook$contributions > median(facebook$contributions))
boxplot(top_50$contributions)
summary(top_50$contributions)

top_25 <- quantile(facebook$contributions, .75)
top_25

#Generate different distributions of contribution for different quantile

facebook$standard_cont <- (facebook$contributions - mean(facebook$contribution))/sd(facebook$contributions)


#States about facebook centrality
summary(facebook$between_centrality)

#hist(facebook$between_centrality)
#boxplot(facebook$between_centrality)

facebook$std_cent <- (facebook$between_centrality - mean(facebook$between_centrality))/sd(facebook$between_centrality)
top_50$deciles <- ntile(top_50$contributions,10)
facebook %>% ggplot(aes(x=between_centrality,y = contributions,color=member)) + geom_point()
top_50 %>% ggplot(aes(x=as.factor(deciles),y=log10(contributions))) + geom_boxplot()



#Do members of Facebook contribute more to repos?
(facebook %>% group_by(member) %>% summarise(mean_cont = mean(contributions)))

#Are members of Facebook more central?


#What happens if we exclude facebook members?



tensorflow <- read.csv("Tensorflow_final.csv")

tensorflow %>% filter(contributions < 3000) %>% ggplot(aes(x=between_centrality,y = contributions,color=member)) + geom_point()

tensorflow$deciles <- ntile(tensorflow$contributions,10)
tensorflow %>% ggplot(aes(x=as.factor(deciles),y=log10(contributions))) + geom_boxplot()
boxplot(facebook$between_centrality)
