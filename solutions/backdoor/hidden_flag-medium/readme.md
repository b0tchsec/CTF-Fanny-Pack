In the binary, I found a function called get_flag().
So I decided it would be easiest to patch the binary.
I replaced the 'call _printf' line, with 'call get_flag'.
Applied the patch to the binary and re-executed it.
Flag acquired!
