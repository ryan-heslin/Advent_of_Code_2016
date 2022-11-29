raw_input <- read.table("inputs/day6.txt", sep = "")
processed <- strsplit(raw_input[[1]], split = "") |>
    do.call(what = rbind)

select_level <- function(x, fun) {
    counts <- table(x)
    names(counts[counts == fun(counts)])
}

part1 <- apply(processed, MARGIN = 2, FUN = select_level, fun = max) |> paste(collapse = "")

print(part1)

part2 <- apply(processed, MARGIN = 2, FUN = select_level, fun = min) |> paste(collapse = "")
print(part2)
