private static SerialPort port;
private static bool _continue = false;

public static void Main(string[] args)
{
    port = new SerialPort();
    port.PortName = "COM8";
    port.BaudRate = 115200;
    port.Parity = Parity.None;
    port.DataBits = 8;
    port.StopBits = StopBits.One;
    port.Handshake = Handshake.None;
    port.RtsEnable = true;
    port.DtrEnable = true;
    port.ReadTimeout = 500;
    port.WriteTimeout = 500;
    port.Open();

    _continue = true;
    Thread thr = new Thread(SerialPortProgram);
    thr.Start();

}


private static void SerialPortProgram()
{
    Console.WriteLine("Writing to port: <SYN>T<CR><LF>");
    string command = "<SYN>T<CR><LF>";
    port.WriteLine(command);

     while (_continue)
    {
        try
        {
           string input = port.ReadLine();
           Console.WriteLine("Input is - " + input);

        }
        catch (TimeoutException) { }
    }

}