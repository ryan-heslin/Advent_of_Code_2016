validate_triangle <- function(x) {
    sum(x) > 2 * max(x)
}

raw_input <- read.table("inputs/day3.txt")
by_row <- asplit(raw_input, MARGIN = 1)

part1 <- vapply(by_row, validate_triangle, FUN.VALUE = logical(1)) |>
    sum()

print(part1)

part2 <- split(raw_input, (seq_len(nrow(raw_input)) - 1) %/% 3) |>
    vapply(\(x) vapply(x, validate_triangle, FUN.VALUE = logical(1)),
        FUN.VALUE = logical(3)
    ) |>
    sum()

print(part2)
