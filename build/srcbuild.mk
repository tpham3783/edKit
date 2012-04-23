C_OBJS = $(SRCS:.c=.o)
CXX_OBJS = $(CXX_SRCS:.cpp=.o)
OBJS = $(C_OBJS) $(CXX_OBJS)

TARGET_NAME = $(NAME)
ifeq ($(BUILD_TYPE),staticlib)
TARGET_NAME = lib$(NAME).a
else
ifeq ($(BUILD_TYPE),dynlib)
TARGET_NAME = lib$(NAME).so
endif
endif

all: $(BUILD_TYPE)

exe: $(OBJS)
	$(CXX) -o $(NAME) $(OBJS) $(LDFLAGS)

staticlib: $(OBJS)
	$(AR) -rcs lib$(NAME).a $(OBJS)

dynlib: $(OBJS)
	$(CXX) -shared -Wl,-soname,$(NAME) -o lib$(NAME).so $(OBJS) $(LDFLAGS)

clean:
	rm -f $(C_OBJS)
	rm -f $(CXX_OBJS)
	rm -f $(TARGET_NAME)

%.o : %.c
	$(CC) $(CPPFLAGS) $(CFLAGS) -o $@ -c $<

%.o : %.cpp
	$(CXX) $(CPPFLAGS) $(CFLAGS) $(CXXFLAGS) -o $@ -c $<