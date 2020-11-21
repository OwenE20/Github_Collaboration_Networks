library(tidyverse)
library(ggplot2)
library(gridExtra)

facebook <- read.csv("Facebook_final.csv")
tensorflow <- read.csv("Tensorflow_final.csv")

facebook$org <- "facebook"
tensorflow$org<- "tensorflow"

full <- rbind(facebook,tensorflow)


#Generate different distributions of contribution for different quantile
  
  

standardize <- function(metric){
  return((metric - mean(metric))/sd(metric))
}


standard_summary <- function(df){
  
  cent_v_df <- df %>% ggplot(aes(x=centrality,y = contributions, color=member)) + geom_point() 
  dist_cent <- df %>% filter(centrality > 0) %>% ggplot(aes(x=member,y = log10(centrality)) )+ geom_boxplot()
  dist_cont <- df %>% filter(centrality > 0) %>%ggplot(aes(x=member,y = log10(contributions))) + geom_boxplot()   
  
  grid.arrange(cent_v_df,dist_cont,dist_cent,nrow=3)
  #figuret out better layout
  return(df)
  
}


facebook <- standard_summary(facebook)

quantile_summaries <- function(df){
  #In the future, make this more flexible, specify columns
  
  df$cont_deciles <- ntile(df["contributions"],10)
  df$cent_deciles <- ntile(df["centrality"],10)
  
  
  #Facet Wrap membershup?
  cont_g <- df %>% ggplot(aes(x=as.factor(cont_deciles),y=log10(contributions))) + geom_boxplot() +facet_wrap(~member)+ ggtitle(df$org)
  cent_g <- df %>% ggplot(aes(x=as.factor(cent_deciles),y=log10(centrality))) + geom_boxplot()+facet_wrap(~member)
  
  grid.arrange(cent_g,cont_g,nrow=2)
  
  #q_q <- df %>% ggplot()
  
}

quantile_summaries(facebook)

#exclude gardener
tensorflow <- filter(tensorflow, contributions < 30000)
tensorflow <- standard_summary(tensorflow)
quantile_summaries(tensorflow)

(facebook %>% group_by(member) %>% summarise(med_cont = median(contributions),
                                             med_cent = median(centrality),
                                             iqr_cent = IQR(centrality),
                                             iqr_cont = IQR(contributions)))
  

top_50 <- facebook %>% filter(contributions > median(contributions))
top_50 <- standard_summary(top_50)
quantile_summaries(top_50)

(top_50 %>% group_by(member) %>% summarise(med_cont = median(contributions),
                                             med_cent = median(between_centrality),
                                             iqr_cent = IQR(between_centrality),
                                             iqr_cont = IQR(contributions)))





full_df$member <- as.logical(full_df$member)
member_prop <- full_df %>% filter(org == "facebook" & member==T)
sum(member_prop$contributions)/sum(full_df$contributions)
  

full_df<- full_df %>%
  mutate(totalPullRequestReviewContributions = as.numeric(totalPullRequestReviewContributions)) %>%
  mutate(totalIssueContributions = as.numeric(totalIssueContributions)) %>%
  mutate(totalRepositoriesWithContributedCommits = as.numeric(totalRepositoriesWithContributedCommits))

#sum(member_prop$totalPullRequestReviewContributions)/sum(full_df$totalPullRequestReviewContributions)


a <- full_df %>% ggplot(aes(x=centrality,y = totalPullRequestReviewContributions,color= member)) + geom_point() + facet_wrap(~org)
b <- full_df %>% ggplot(aes(x=member,y = log10(totalPullRequestReviewContributions)) )+ geom_boxplot() + facet_wrap(~org)
c <- full_df %>% ggplot(aes(x=member,y = log10(totalRepositoriesWithContributedCommits))) + geom_boxplot()   + facet_wrap(~org)

grid.arrange(a,b,c,nrow=3)



facebook_raw <- read.csv("facebook_raw.csv")

counts <- facebook_raw %>% group_by(repo) %>% summarise(members = n())
summary(counts)

tensorc <- read.csv("tensorflow_raw.csv")

counts_t <- tensorc %>% group_by(repo) %>% summarise(members = n())
summary(counts_t)


full_df %>% filter(centrality > 0) %>% ggplot(aes(x=member,y = log10(centrality)) )+ geom_boxplot() + facet_wrap(~org)
