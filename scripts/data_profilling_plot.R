library(dplyr)
library(ggplot2)

gas = read.csv('fuel_card_export-csv.csv')
dt_brand <- gas %>%
  group_by(Merchant.Brand) %>%
  filter(n() > 100) %>%
  ungroup()

dt_brand = dt_brand[(dt_brand$Product.Class=='Unleaded')&(dt_brand$Distance.Driven < 350)&(dt_brand$Distance.Driven > 100),c('Merchant.Brand','Total.Fuel.Cost','Units','Distance.Driven')]
dt_brand['dpd'] = dt_brand$Distance.Driven / dt_brand$Total.Fuel.Cost
dpd_sd = sd(dt_brand$dpd)
dt_brand['dpg'] = dt_brand$Distance.Driven / dt_brand$Units
dpg_sd = sd(dt_brand$dpg)
brand_cost_distance = aggregate(dt_brand[,c('Total.Fuel.Cost','Distance.Driven','Units')], by=list(dt_brand$Merchant.Brand), sum)
brand_cost_distance = aggregate(dt_brand[,c('Total.Fuel.Cost','Distance.Driven','Units')], by=list(dt_brand$Merchant.Brand), sum)
#brand_cost_distance = aggregate(dt_brand[,c('dpd','dpg')], by=list(dt_brand$Merchant.Brand), mean)

brand_cost_distance['DistancePerDollar'] = brand_cost_distance$Distance.Driven / brand_cost_distance$Total.Fuel.Cost 
brand_cost_distance['DistancePerGallon'] =  brand_cost_distance$Distance.Driven / brand_cost_distance$Units

da$EX <- factor(da$EX, levels = da$EX[order(-da$X208.37999999999997)])

brand_cost_distance$Group.1 = factor(brand_cost_distance$Group.1, levels = brand_cost_distance$Group.1[order(-brand_cost_distance$DistancePerDollar)])
ggplot(data=brand_cost_distance, aes(x=Group.1, y=DistancePerDollar, fill=Group.1)) +
  geom_bar(stat='identity', width = 0.6) +
  geom_text(aes(label=round(DistancePerDollar,2)),vjust=-0.3, size=6,color="black",) +
  ggtitle('Total distance driven vs. Fuel cost') + scale_fill_brewer(palette="Oranges") + theme_minimal() +
  theme(axis.title.x=element_blank(),
        axis.text.x=element_blank(),
        axis.ticks.x=element_blank(),
        legend.text=element_text(size=16))

brand_cost_distance$Group.1 = factor(brand_cost_distance$Group.1, levels = brand_cost_distance$Group.1[order(-brand_cost_distance$DistancePerGallon)])
ggplot(data=brand_cost_distance, aes(x=Group.1, y=DistancePerGallon, fill=Group.1)) +
  geom_bar(stat='identity', width = 0.6) +
  geom_text(aes(label=round(DistancePerGallon,2)),vjust=-0.3, size=6,color="black",) +
  ggtitle('Total distance driven vs. Fuel volume') + scale_fill_brewer(palette="Greens") + theme_minimal() +
  theme(axis.title.x=element_blank(),
        axis.text.x=element_blank(),
        axis.ticks.x=element_blank(),
        legend.text=element_text(size=16))

city_month = read.csv('city_month.csv')
city_month$Merchant.City <- factor(city_month$Merchant.City, levels = city_month$Merchant.City[order(-city_month$Unit.Cost)])
ggplot(data=city_month, aes(x=Merchant.City, y=Unit.Cost, fill=Merchant.City)) +
  geom_bar(stat='identity', width = 0.6, show.legend=F) +
  geom_text(aes(label=round(Unit.Cost,2)),vjust=-0.3, size=6,color="black",) +
  ggtitle('Average fuel unit cost') + scale_fill_brewer(palette="RdYlGn") + theme_minimal()+
  theme(axis.text.x=element_text(size=16))

da = read.csv('department_annualcost.csv')
da$EX <- factor(da$EX, levels = da$EX[order(-da$X208.37999999999997)])
ggplot(data=da, aes(x=EX , y=X208.37999999999997, fill=EX)) +
  geom_bar(stat='identity', width = 0.6, show.legend = F) +
  geom_text(aes(label=round(X208.37999999999997,2)), vjust = -.3, size=6,color="black",) +
  ylab('Cost') +
  ggtitle('Departments annual cost') + scale_fill_brewer(palette="RdYlGn") + theme_minimal() +
  theme(axis.text.x=element_text(size=16))
save.image('Departments annual cost.png')
