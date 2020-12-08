## FMA_mediumデータセットの楽曲からChipと名前のつくジャンルの曲を抽出する

library(tidyverse)
# setwd("/home/matsumoto/Documents/data/music/fma")

## メタデータの読み込み
metadata <- read_csv("fma_metadata/tracks.csv", skip = 1)
metadata_tbl <- metadata %>% tibble()
metadata_tbl %>% select(genre_top) %>% table()
## ジャンルデータの読み込み
genredata <- read_csv("fma_metadata/genres.csv", skip = 0)
genredata_tbl <- genredata %>% tibble()
## chipと名前がつくジャンルのジャンルidを取得
genredata_tbl %>% filter(str_detect(title, regex("chip", ignore_case = T)))
genre_chip_ids <- genredata_tbl %>% filter(str_detect(title, regex("chip", ignore_case = T))) %>% .$genre_id
## 
chips <- metadata_tbl %>% filter(str_detect(genres, paste(as.character(genre_chip_ids), collapse = "|"))) %>% filter(genre_top == "Electronic") %>% filter(subset == "medium")

## すべての楽曲ファイルのパスを取得
files_path <- list.files("fma_medium", recursive = T, full.names = T)
files_path <- files_path[files_path %>% str_detect(".mp3")]

## ファイル名からファイルIDを抽出
files_id <- files_path %>% substr(17, 22) %>% str_remove_all("^0*")

chips_file_list <- files_path[files_id %in% chips$X1]

## コピー先のディレクトリを作成
dir.create("fma_medium_separated/")
dir.create(paste0("fma_medium_separated/", "Chip/"))

## ファイル名をGTZANと同様のフォーマットになるようにしてコピーする
for (i in seq_along(chips_file_list)) {
  dest_dir <- paste0("fma_medium_separated/", "Chip/")
  file.copy(chips_file_list[i], paste0(dest_dir, "Chip.", str_extract(chips_file_list[i], "[0-9]{6}.*")))
}
