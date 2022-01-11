# Khai bao thu vien
install.packages("ggplot2", lib="C:\\Users\\acer\\Downloads\\R\\win-library\\3.3")
update.packages("ggplot2")
install.packages("plotly")
library(tidyverse)
library(plotly)
library(dplyr)
library(ggplot2)

# Doc file du lieu
setwd("C:\\Users\\acer\\lazada_laptop\\lazada_laptop")
dt <- read.csv("lazada_out_R.csv",encoding = "UTF-8" , header = T, stringsAsFactors = F) 
view(dt)

#Tong quan ve du lieu
summary(dt)
#Tao cac ham tinh mean, mode, median, var, sd, min, max, range
desc <- function(x)
{
  tb <- mean(x)
  tv <- median(x)
  ps <- var(x)      
  dlc <- sd(x)     
  tn <- min(x)
  ln <- max(x)
  tc <- range(x)  
  c(MEAN = tb,  MEDIAN = tv, VAR = ps,
    SD = dlc, MIN = tn, MAX = ln, RANGE = tc)
}
desc(dt$price)
desc(dt$original_price)
desc(dt$response_rate)
desc(dt$delivered_on_time)
desc(dt$discount_price)
desc(dt$p_rating)
desc(dt$shipping_fee)

getmode <- function(v, na.rm = TRUE) {
  uniqv <- unique(v)
  uniqv[which.max(tabulate(match(v, uniqv)))]
}
getmode(dt$price)
getmode(dt$original_price)
getmode(dt$response_rate)
getmode(dt$delivered_on_time)
getmode(dt$discount_price)
getmode(dt$p_rating)
getmode(dt$shipping_fee)

# Tao cac list chua tong cua tung du lieu trong tap du lieu
sum_dt <- c(sum(dt$price),
            sum(dt$original_price),
            sum(dt$response_rate),
            sum(dt$delivered_on_time),
            sum(dt$discount_price),
            sum(dt$p_rating),
            sum(dt$shipping_fee))
          
sum_dt_names <- c("price",
                  "original_price",
                  "response_rate",
                  "delivered_on_time",
                  "discount_price",
                  "p_rating",
                  "shipping_fee")
                  
#Tao data frame tu 2 list tren
dt_1 <- data.frame(sum_dt, sum_dt_names)

# BD1: Ve bieu do the hien tong gia tri cua tung du lieu dinh luong cua tap du lieu
ggplot(dt_1, aes(x = sum_dt_names, y = sum_dt, fill = sum_dt_names)) +
  geom_col(position = "stack") +
  geom_text(aes(label=sum_dt), vjust=0) +
  scale_y_log10() +
  labs(title="TONG GIA TRI CUA DU LIEU DINH LUONG",
       x = "Columns",
       y = "Count")

#BD2_Bieu do cot:
  # Do thi the hien tong gia san pham cua tung thuong hieu
ggplot(dt, aes(x=brand, y=price))  + 
  geom_col(aes(fill =brand)) + 
  xlab("brand")+
  ylab("price")+
  labs(title="DO THI THE HIEN TONG GIA SAN PHAM CUA TUNG THUONG HIEU ")
  theme(axis.text.x = element_text(size = 8, angle = 90))+

# BD3_Bieu do diem
  # Bieu do the hien ty le danh gia tich cuc doi voi nha ban hang 
ggplot(dt, aes(x= p_rating,y= s_name ))+
   geom_point(aes(color = s_name))+
   ylab("nha ban hang")+
   xlab("danh gia tich cuc")+
   labs(title="BIEU DO THE HIEN TY LE DANH GIA TICH CUC DOI VOI NHA BAN HANG ")
  
# BD4_Bieu do cot:
 # Bieu do the hien ty le phan hoi cua nha ban hang
ggplot(dt, aes(y = s_name , x=response_rate, fill = s_name  )) +
   geom_col() + 
   labs(title = "BIEU DO THE HIEN TY LE PHAN HOI CUA NHA BAN HANG ")

# Tao cac list theo tung muc gia tu thap nhat den cao nhat 
Low = subset(dt[,9], dt$price <= 150)
avg = subset(dt[,9], dt$price <= 300 & dt$price > 150)
high = subset(dt[,9], dt$price > 300)


#Tao list chua length cua tung muc do gia
price <- c(length(Low),
           length(avg),
           length(high))
price_classify <- c("Low",
                    "Average",
                    "High")
#tao data frame tu 2 list tren
dt_2 <- data.frame(price, price_classify)

#BD5_Bieu do cot:
    # Bieu do the hien so luong gia san pham danh gia theo moi cap do 
ggplot(dt = dt_2, mapping = aes(x = price, y = price_classify, fill= price_classify)) +
  geom_col() +
  labs(title="BIEU DO THE HIEN SO LUONG GIA SAN PHAM DANH GIA THEO MOI CAP DO")

#BD6_Bieu do diem:
  # Do thi the hien phi van chuyen cua nha ban hang
ggplot(dt, aes(y=s_name, x=shipping_fee))+
  geom_point(aes(colour = s_name),
             colour = "orange")+
  xlab("nha ban hang")+
  ylab("phi van chuyen")+
  labs(title="DO THI THE HIEN PHI VAN CHUYEN CUA NHA BAN HANG") 

# BD7_Bieu do cot chong
    # Bieu do the hien tuong quan giua ty le phan hoi và danh gia tich cuc
fig <- plot_ly(dt, x = ~s_name)
fig <- fig %>% add_trace(y = ~p_rating, name = 'danh gia tich cuc',mode = 'lines')
fig <- fig %>% add_trace(y = ~response_rate, name = 'phan hoi', mode = 'lines+markers')
fig <- fig %>% layout(yaxis = list(title = 'Count'), barmode = 'stack')
fig <- fig %>% layout(title = "BIEU DO THE HIEN TUONG QUAN GIUA TY LE PHAN HOI VÀ DANH GIA TICH CUC")
fig
