# Use this to create df with both contract data and player stats

library(rvest)
library(dplyr)
library(caret)

#function for turning contract character strings into numeric
convert <- function(x) {
  x <- gsub('[$]',"",x)
  x <- gsub('[,]',"",x)
}

# removing duplicates in bball-reference database that show from player being traded
remove_duplicates <- function(x) {
  traded_guys <- x %>% filter(Tm == "TOT") # save traded players total season
  x <- x %>%
    group_by(Player) %>% 
    filter(n() == 1) # delete all instances of a player that shows up more than once
  x <- rbind(x,traded_guys) # add back the full season of players that got traded
}

#scrape contract data from spotrac
contracts_page <- read_html("https://www.spotrac.com/nba/free-agents/2022/")
players <- contracts_page %>% html_nodes(".player a") %>% html_text()
players[1:91] 
years <- contracts_page %>% html_nodes(".center:nth-child(7)") %>% html_text()
years[3:93] 

salary <- contracts_page %>% html_nodes(".result+ .center") %>% html_text()
for(i in 1:length(salary)) {
  salary[i] = convert(salary[i])
}
full_salary<-as.numeric(salary[seq(2,182,2)]) #adjust based on how many players actually got a contract
avg_salary <- as.numeric(salary[seq(1,181,2)])

#create df with player, contract length, avg salary and total salary
contract_df <- as.data.frame(players[1:91])
colnames(contract_df) <- "Player"
contract_df$Years <- years[3:93]
contract_df$Full_Salary <- full_salary
contract_df$Avg_Salary <- avg_salary

#get per game stats of contract year from bball reference
per_game <- read.csv("https://raw.githubusercontent.com/mkarlthayer/basketball/main/bball_per_game_2022.txt")
per_game <- remove_duplicates(per_game)
per_game <- per_game[-c(1,31)] #remove irrelevant columns

#get advanced stats of contract year from bball reference
advanced <- read.csv("https://raw.githubusercontent.com/mkarlthayer/basketball/main/bball_advanced_2022.txt")
advanced <- remove_duplicates(advanced)
advanced <- advanced[-c(1,3:7,30)] #remove irrelevant and repeated columns

# combine advanced and per_game stats
stats <- merge(per_game, advanced, by = "Player")
# combine the stats with the contract data
df <- merge(contract_df, stats, by = "Player")
# save as csv
write.csv(df, "C:/Users/kthay/Downloads/2022_NBA_Contracts.csv")

