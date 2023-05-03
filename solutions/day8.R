execute <- function(grid, instructions) {
    parse <- function(line) {
        parts <- strsplit(line, "\\s") |>
            unlist()
        if (parts[[1]] == "rect") {
            bounds <- strsplit(parts[[2]], "x") |>
                unlist() |>
                strtoi()
            function() rect(bounds[[1]], bounds[[2]])
        } else {
            target <- strsplit(parts[[3]], "=") |>
                unlist() |>
                tail(1) |>
                strtoi()
            n <- strtoi(parts[[5]])
            func <- if (parts[[2]] == "row") rotate_row else rotate_column
            function() func(target + 1, n)
        }
    }


    rotate_vector <- function(x, n) {
        len <- length(x)
        cutpoint <- len - n + 1
        right <- x[cutpoint:len]
        left <- x[1:(cutpoint - 1)]
        c(right, left)
    }

    rect <- function(x, y) {
        grid[1:y, 1:x] <<- 1
    }


    rotate_row <- function(row, n) {
        grid[row, ] <<- rotate_vector(grid[row, ], n)
    }

    rotate_column <- function(col, n) {
        grid[, col] <<- rotate_vector(grid[, col], n)
    }

    instructions <- lapply(raw_input, parse)
    for (line in instructions) {
        line()
    }
    grid
}
raw_input <- readLines("inputs/day8.txt")
nrow <- 6
ncol <- 50
grid <- matrix(0, nrow = nrow, ncol = ncol)
grid <- execute(grid, raw_input)

part1 <- sum(grid)
print(part1)

apply(grid, MARGIN = 2, FUN = rev) |>
    t() |>
    image()
