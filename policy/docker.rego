package docker

# Get Dockerfile content as lines
lines contains value if {
    value := split(input, "\n")[_]
}

# Rule: No latest tag
deny contains msg if {
    line := lines[_]
    startswith(line, "FROM")
    contains(line, ":latest")
    msg := "FROM should not use :latest tag"
}

# Rule: Images must be pinned
deny contains msg if {
    line := lines[_]
    startswith(line, "FROM")
    not contains(line, ":")
    not contains(line, "@sha256:")
    msg := "FROM must specify a tag or digest"
}

# Rule: No ADD command
deny contains msg if {
    line := lines[_]
    startswith(line, "ADD")
    msg := "Use COPY instead of ADD"
}

# Rule: No secrets in ENV
deny contains msg if {
    line := lines[_]
    startswith(line, "ENV")
    lower_line := lower(line)
    some word in ["secret", "password", "token", "key"]
    contains(lower_line, word)
    msg := sprintf("Possible secret in ENV: %s", [line])
}

# Rule: No SSH port
deny contains msg if {
    line := lines[_]
    startswith(line, "EXPOSE")
    contains(line, "22")
    msg := "SSH port 22 should not be exposed"
}

# Rule: Must have non-root USER
deny contains msg if {
    not has_valid_user
    msg := "Dockerfile must specify non-root USER"
}

has_valid_user if {
    line := lines[_]
    startswith(line, "USER")
    not contains(line, "root")
    not contains(line, "0")
}