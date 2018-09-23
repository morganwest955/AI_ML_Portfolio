function(plot.data){
    v1 = vector(mode="numeric", length = nrow(plot.data))
    v2 = vector(mode="numeric", length = nrow(plot.data))
    v3 = vector(mode="numeric", length = nrow(plot.data))
    v4 = vector(mode="numeric", length = nrow(plot.data))
    v5 = vector(mode="numeric", length = nrow(plot.data))
    col = c("PSC", "PG", "PA", "PSA", "PSH", "PMVP", "APGO", "GPP")
    for(i in (1:nrow(plot.data))){
        v1[i]=euc.dist(plot.data[i,col], bestcluster$centers[1,])
        v2[i]=euc.dist(plot.data[i,col], bestcluster$centers[2,])
        v3[i]=euc.dist(plot.data[i,col], bestcluster$centers[3,])
        v4[i]=euc.dist(plot.data[i,col], bestcluster$centers[4,])
        v5[i]=euc.dist(plot.data[i,col], bestcluster$centers[5,])
    }
    v1max = max(v1)
    v2max = max(v2)
    v3max = max(v3)
    v4max = max(v4)
    v5max = max(v5)
    for(i in (1:nrow(plot.data))){
        v1[i]=(1-(v1[i]/v1max))
        v2[i]=(1-(v2[i]/v2max))
        v3[i]=(1-(v3[i]/v3max))
        v4[i]=(1-(v4[i]/v4max))
        v5[i]=(1-(v5[i]/v5max))
    }
    return(data.frame(Player=plot.data$Player, Team=plot.data$Team, Striker=v1, Passer=v2, Carry=v3, OffensiveMidfield=v4, DefensiveMidfield=v5))
}

calcteamstats <- function(table.data){
    a <- dplyr::summarize(dplyr::group_by(table.data,Team),Score=sum(Score),Goals=sum(Goals),Assists=sum(Assists),Saves=sum(Saves),Shots=sum(Shots),Wins=sum(MVP))
	return(a)
}

calcplayerstats <- function(table.data){
	a <- dplyr::summarize(dplyr::group_by(table.data,Player),Score=sum(Score),Goals=sum(Goals),Assists=sum(Assists),Saves=sum(Saves),Shots=sum(Shots),Wins=sum(Wins),MVP=sum(MVP))
	return(a)
}

calcplayerstats <- function(table.data){
	playerstats <- data.frame(Player=0,Team=0,Score=0,Goals=0,Assists=0,Saves=0,Shots=0,Wins=0,MVPs=0)
	table.data <- table.data[order(table.data$Player),] #orders the table
	playerstats[1,]$Player <- table.data[1,]$Player
	playerstats[1,]$Team <- table.data[1,]$Team
	rowposition = 1	
	for (i in table.data){	
		if(playerstats[rowposition,]$Team != table.data[i,]$Team){
			rowposition = rowposition+1
			playerstats[rowposition,]$Player <- table.data[i,]$Player
			playerstats[rowposition,]$Team <- table.data[i,]$Team
			playerstats[rowposition,]$Score = 0
			playerstats[rowposition,]$Goals = 0
			playerstats[rowposition,]$Assists = 0
			playerstats[rowposition,]$Saves = 0
			playerstats[rowposition,]$Shots = 0
			playerstats[rowposition,]$Wins = 0
			playerstats[rowposition,]$MVPs = 0
		}
		else{
			playerstats[rowposition,]$Score = playerstats[rowposition,]$Score + table.data[i,]$Score
			playerstats[rowposition,]$Goals = playerstats[rowposition,]$Goals + table.data[i,]$Goals
			playerstats[rowposition,]$Assists = playerstats[rowposition,]$Assists + table.data[i,]$Assists
			playerstats[rowposition,]$Saves = playerstats[rowposition,]$Saves + table.data[i,]$Saves
			playerstats[rowposition,]$Shots = playerstats[rowposition,]$Shots + table.data[i,]$Shots
			playerstats[rowposition,]$Wins = playerstats[rowposition,]$Wins + table.data[i,]$Wins
			playerstats[rowposition,]$MVPs = playerstats[rowposition,]$MVPs + table.data[i,]$MVPs
		}
	}
	View(playerstats)
}

calcplayerstats <- function(table.data){
	library(plyr)
	groupColumns = c("Player","Team")
	dataColumns = c("Score","Goals","Assists","Saves","Shots","Wins","MVPs")
	res = ddply(table.data, groupColumns, function(x) colSums(x[dataColumns]))
	View(res)
}