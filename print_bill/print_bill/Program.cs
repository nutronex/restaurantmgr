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
        static List<string[]> data = new List<string[]>();
        static string billid = "";
        static string table = "";
        private void xx(object sender, PrintPageEventArgs arg)
        {
            Graphics g = arg.Graphics;
            Font normar_font = new Font("Zawgyi-One", 7);
            System.Console.WriteLine(data.Count);
            int[] row_width = { 0, 80, 105, 145 };
            DateTime t = DateTime.Now;
            int table_title_Y = 60;

            string billstring = "bill.no: " + billid + " table: " + table;
            g.DrawString("3D Restaurant", new Font("Zawgyi-One", 7), new SolidBrush(Color.Beige), 60, 1);
            g.DrawString(billstring, new Font("Zawgyi-One", 7), new SolidBrush(Color.Beige), 0, table_title_Y - 35); 
            g.DrawString(t.ToString(), new Font("Zawgyi-One", 7), new SolidBrush(Color.Beige), 0, table_title_Y-20);
            g.DrawLine(new Pen(new SolidBrush(Color.Black)), new Point(1, table_title_Y-5), new Point(200, table_title_Y-5));
            g.DrawLine(new Pen(new SolidBrush(Color.Black)), new Point(1, table_title_Y + 20), new Point(200, table_title_Y + 20));

            g.DrawString("item", new Font("Zawgyi-One", 8, FontStyle.Bold), new SolidBrush(Color.Black), row_width[0], table_title_Y);
            g.DrawString("qty", new Font("Zawgyi-One", 8, FontStyle.Bold), new SolidBrush(Color.Black), row_width[1], table_title_Y);
            g.DrawString("price", new Font("Zawgyi-One", 8, FontStyle.Bold), new SolidBrush(Color.Black), row_width[2], table_title_Y);
            g.DrawString("amount", new Font("Zawgyi-One", 8, FontStyle.Bold), new SolidBrush(Color.Black), row_width[3], table_title_Y);
            
            int end_x = 0;
            int total_amount = 0;
            for (int i = 1; i < data.Count + 1; i++)
            {
                end_x = i * 30;
                g.DrawString(data[i - 1][0], new Font("Zawgyi-One", 5), new SolidBrush(Color.Black), row_width[0], end_x + table_title_Y + 2);
                g.DrawString(data[i - 1][2], normar_font, new SolidBrush(Color.Black), row_width[1], end_x + table_title_Y);
                g.DrawString(data[i - 1][1], normar_font, new SolidBrush(Color.Black), row_width[2], end_x + table_title_Y);
                int total = int.Parse(data[i - 1][1]) * int.Parse(data[i - 1][2]);
                total_amount += total;
                g.DrawString(total.ToString(), normar_font, new SolidBrush(Color.Black), row_width[3], end_x + table_title_Y);
                
            }

            

            g.DrawLine(new Pen(new SolidBrush(Color.Black)), new Point(1, end_x + 80), new Point(200, end_x + 80));
            g.DrawLine(new Pen(new SolidBrush(Color.Black)), new Point(100, end_x + 80), new Point(100, end_x + 110));
            g.DrawString("total amount", normar_font, new SolidBrush(Color.Black), row_width[0], end_x + 90);
            g.DrawString(total_amount.ToString(), normar_font, new SolidBrush(Color.Black), row_width[2]+20, end_x + 90);
            g.DrawLine(new Pen(new SolidBrush(Color.Black)), new Point(1, end_x + 110), new Point(200, end_x + 110));

            g.DrawString("thanks you :) ", normar_font, new SolidBrush(Color.Beige), 50, end_x + 120);
        }


        private List<string[]> parseData(string s)
        {
            Regex pattern = new Regex(@"\s*\]\s*,\s*\[\s*");
            s = s.Replace("]]", "|").Replace("[[", "|");
            string str = pattern.Replace(s, "|");
          //  System.Console.WriteLine(str);
            string[] arr = str.Split('|');

            List<string[]> l = new List<string[]>();
            foreach (string x in arr)
            {
                if (x != "")
                {
                    string[] j = x.Split(',');
                    l.Add(j);
                }
            }
            return l;
        }

        public void print()
        {
            PrintDocument pdoc = new PrintDocument();
            PrinterSettings.StringCollection px = PrinterSettings.InstalledPrinters;
            List<string> printerlist = new List<string>();
            foreach (string x in px)
            {
                printerlist.Add(x);
            }
            if (printerlist.Count >= 2)
            {
            //    pdoc.PrinterSettings.PrinterName = printerlist[0];
                //System.Console.WriteLine(printerlist[0]);
            }
            pdoc.PrintPage += new PrintPageEventHandler(xx);
            pdoc.Print();

        }

       
        static void Main(string[] args)
        {
         //   string strx = "[[cocktail,8,2500,969 ]   , [beer,3,2500,969]]";
            string str = "";
            for (int i = 0; i < args.Length; i++)
            {
                str += args[i];
            }
          //  System.Console.WriteLine("start--------------------------");
            Program x = new Program();
//            string xstr = "[['ၾကက္နံခ်ဥ္စပ္', 7200, 31]]@284:5";
        //    System.Console.WriteLine(str);
            string[] str_array = str.Split('@');
           // foreach (string i in str_array) { System.Console.WriteLine(i); }
            string[] str_bill_table = str_array[1].Split(':');
            billid = str_bill_table[0];
            table = str_bill_table[1];
            data = x.parseData(str_array[0]);
            x.print();


        //    System.Console.WriteLine("end------------------------------");
           // System.Console.ReadLine();

        }
    }
}
