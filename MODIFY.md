其实就改了`wiringPi.c`文件里的一个函数。       

```c
unsigned int digitalReadByte (void)
{
  int pin, x ;
  uint32_t raw ;
  uint32_t data = 0 ;

  /**/ if (wiringPiMode == WPI_MODE_GPIO_SYS)
  {
    for (pin = 0 ; pin < 8 ; ++pin)
    {
      x = digitalRead (pinToGpio [pin]) ;
      data = (data << 1) | x ;
    }
  }
  else
  {
    raw = *(gpio + gpioToGPLEV [0]) ; // First bank for these pins
    for (pin = 0 ; pin < 8 ; ++pin)
    {
      x = pinToGpio [pin] ;
      data = (data << 1) | (((raw & (1 << x)) == 0) ? 0 : 1) ;
    }
  }
  return data ;
}
```

上面是 [原wiringPi-python包](https://github.com/WiringPi/WiringPi-Python) 的`unsigned int digitalReadByte (void)`函数，它读取wiringPi编码的0~7号管脚，并返回整形int数据类型。
在从FIFO里读取AD采样数据时，要求一次读12bit（AD9233是12位宽的模数转换器），因此改为下面的代码。      

```c
unsigned int digitalReadByte (void)
{
  int ret;
  ret = *(gpio + gpioToGPLEV [0]);
  return (ret & 127) + ((ret>>5) & 3968);
}
```

上面的函数是把BCM编码GPIO的0-6号和12-16设为AD转换结果的0~11位，即     
```verilog
assign AD_INPUT = {BCM[16:12],BCM[6:0]};
```

在安装`wiringPi-python`时，不使用`pip`的安装方式，而是先用`Git`下拉软件包：      

```shell
git clone --recursive https://github.com/WiringPi/WiringPi-Python.git
```

找到`wiringPi.c`里的`unsigned int digitalReadByte (void)`函数，手动替换，然后再安装：      

```shell
sudo apt install swig
sudo python3 setup.py install
```
即可。
