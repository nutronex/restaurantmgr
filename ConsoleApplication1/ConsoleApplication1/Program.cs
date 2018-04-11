using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Drawing.Printing;
using System.Drawing;
using System.Text.RegularExpressions;
namespace ConsoleApplication1
{
    class Program
    {
        private void xx(object sender, PrintPageEventArgs arg) {
            Graphics g = arg.Graphics;
            int[] x = { 10,130,160 };
            DateTime t = DateTime.Now;


            g.DrawString(t.ToString(), new Font("Zawgyi-One", 8), new SolidBrush(Color.Beige), 10, 1);
            g.DrawString("item", new Font("Zawgyi-One", 8, FontStyle.Bold), new SolidBrush(Color.Black), x[0], 20);
            g.DrawString("qty", new Font("Zawgyi-One", 8, FontStyle.Bold), new SolidBrush(Color.Black), x[1], 20);
            g.DrawString("table", new Font("Zawgyi-One", 8, FontStyle.Bold), new SolidBrush(Color.Black), x[2], 20);
            int end_x=0;
          
            for (int i = 1; i < data.Count + 1; i++)
            {
                for (int j =0;j< data[i-1].Length ;j++ )
                {
                     end_x = i*30;
                     g.DrawString(data[i-1][j], new Font("Zawgyi-One", 7), new SolidBrush(Color.Black), x[j], end_x);
                }
            }
            g.DrawString("-------------xx------------", new Font("Arial", 10), new SolidBrush(Color.Beige), 40, end_x+20);
        }


        private List<string[]> parseData(string s)
        {
            Regex pattern = new Regex( @"\s*\]\s*,\s*\[\s*");
            s = s.Replace("]]", "|").Replace("[[", "|");
          //  System.Console.WriteLine(s);
            string str = pattern.Replace(s, "|");
            string[] arr = str.Split('|');
            List<string[]> l = new List<string[]>(); 
            foreach (string x in arr) {
              //  string i =new Regex(@"\'\w+\':").Replace(x, "");
                string[] j = x.Split(',');
                l.Add(j);    
          }

            return l;
    
        }
        
        public void print(){
        PrintDocument pdoc = new PrintDocument();
        //pdoc.PrinterSettings.PrinterName="\\\\Net\\XP-58";
        //  pdoc.PrinterSettings.PrinterName = "\\\\Net\\XP-58";
        PrinterSettings.StringCollection px = PrinterSettings.InstalledPrinters;
        List<string> printerlist = new List<string>();
        foreach (string x in px) {
            System.Console.WriteLine(x);
             printerlist.Add(x);
        }

        pdoc.PrintPage += new PrintPageEventHandler(xx);
        if (printerlist.Count >= 2)
        {
            pdoc.PrinterSettings.PrinterName =  printerlist[0];
            if (!pdoc.PrinterSettings.IsDefaultPrinter){
                System.Console.WriteLine("1 not def");
                pdoc.Print();
            }else{
                System.Console.WriteLine("2");
                pdoc.PrinterSettings.PrinterName =  printerlist[1];
                pdoc.Print();
            }
          
        }
         
            
       
           
        }

        static List<string[]> data = new List<string[]>();
        static void Main(string[] args)
        {
     
            string str = "";
            for (int i = 0; i < args.Length; i++) {
                str += args[i];

            }
          
            Program x = new Program();
            string strx = "['??????????????????',2,2]";
            data=x.parseData(strx);            
            x.print();
            System.Console.ReadLine();
            
        }
    }
}
