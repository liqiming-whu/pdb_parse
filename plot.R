#!/usr/bin/env Rscript
library(ggplot2)

args <- commandArgs(T)

tsv <- args[1]
num <- args[2]
out <- args[3]

struc = read.csv(tsv, sep='\t', header=T)
maxnum = as.numeric(readLines(num))
ellip = data.frame(x=0:maxnum-1, y=0:maxnum-1)

p <- ggplot() +
  geom_path(data=ellip, mapping = aes(x=x, y=y), size=0.1, color="black") +
  geom_point(data=struc, mapping = aes(x=plot_x, y=plot_y), size=1, shape=".") +
  geom_point(data=struc, mapping = aes(x=plot_y, y=plot_x), size=1, shape=".") +
  geom_abline(slope = 1, intercept = 0, size=0.1, color="black") +
  labs(x="Read Length", y="Read Length") +
  theme_bw() +
  geom_abline(slope = 1, intercept = 0, size=0.1, color="black") +
  theme(
    text = element_text(family="ArialMT", color = "black", size = 5), 
    panel.background = element_blank(),
    panel.grid = element_blank()
  )

ggsave(file.path(out), p, width = 8, height = 8, limitsize = FALSE, units = "cm")