# Compiles to .so (linux) or .dll (windows) depending on this variable
TARGET = linux

ifeq ($(TARGET),linux)
CC = gcc
CFLAGS = -Wall -std=c99 -fPIC
endif

ifeq ($(TARGET),windows)
CC = x86_64-w64-mingw32-gcc
CFLAGS = -Wall -std=c99
endif

SRC_DIR = src
OUT_DIR = out
LIB_DIR = lib
DEPS_DIR = deps

SRC = main.c
OBJ := $(patsubst %.c, %.o, $(SRC))

# Library name
NAME = assets

ifeq ($(TARGET),linux)
all: $(LIB_DIR)/$(NAME).so
endif

ifeq ($(TARGET),windows)
all: $(LIB_DIR)/$(NAME).dll
endif

$(DEPS_DIR)/stb_image.h: $(DEPS_DIR)
	curl https://raw.githubusercontent.com/nothings/stb/f58f558c120e9b32c217290b80bad1a0729fbb2c/stb_image.h -o $(DEPS_DIR)/stb_image.h

$(DEPS_DIR)/stb_image_write.h: $(DEPS_DIR)
	curl https://raw.githubusercontent.com/nothings/stb/f58f558c120e9b32c217290b80bad1a0729fbb2c/stb_image_write.h -o $(DEPS_DIR)/stb_image_write.h

ifeq ($(TARGET),linux)
$(OUT_DIR)/%.o: $(SRC_DIR)/%.c $(DEPS_DIR)/stb_image.h $(DEPS_DIR)/stb_image_write.h | $(OUT_DIR)
	$(CC) $(CFLAGS) -c $< -o $@
endif

ifeq ($(TARGET),windows)
$(OUT_DIR)/%.win32.o: $(SRC_DIR)/%.c $(DEPS_DIR)/stb_image.h $(DEPS_DIR)/stb_image_write.h | $(OUT_DIR)
	$(CC) $(CFLAGS) -c $< -o $@
endif

# .so
ifeq ($(TARGET),linux)
$(LIB_DIR)/$(NAME).so: $(patsubst %.o, $(OUT_DIR)/%.o, $(OBJ)) | $(LIB_DIR)
	$(CC) -shared $^ -o $@
endif

# .dll
ifeq ($(TARGET),windows)
$(LIB_DIR)/$(NAME).dll: $(patsubst %.o, $(OUT_DIR)/%.win32.o, $(OBJ)) | $(LIB_DIR)
	$(CC) -shared $^ -o $@ -static
endif

$(OUT_DIR):
	mkdir -p $(OUT_DIR)

$(LIB_DIR):
	mkdir -p $(LIB_DIR)

$(DEPS_DIR):
	mkdir -p $(DEPS_DIR)

clean:
	rm -rf $(OUT_DIR) $(LIB_DIR) $(DEPS_DIR)

.PHONY: clean
