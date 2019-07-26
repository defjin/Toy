using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using PdfSharp;
using PdfSharp.Drawing;
using PdfSharp.Pdf;
using PdfSharp.Pdf.IO;
using PdfSharp.Pdf.Content;
using PdfSharp.Pdf.AcroForms;
using System.Diagnostics;
using System.IO;


namespace PDFTranslateInDesktop
{
    public partial class Form1 : Form
    {
        List<PdfDocument> onePageDocumentList = new List<PdfDocument>();
        int _pageCount =0;
        string totalString = "";
        
        public Form1()
        {
            InitializeComponent();
            TranslateButton.Enabled = false;
            richTextBox1.Font = new Font(FontFamily.GenericSansSerif, 14);
            FontSizeBox.Text = "14";
        }

        private void OpenButton_Click(object sender, EventArgs e)
        {
            richTextBox1.Text = "";
            totalString = "";
            _pageCount = 0;
            onePageDocumentList.Clear();
            using (OpenFileDialog dialog = new OpenFileDialog() { ValidateNames = true, Multiselect = false, Filter = "PDF|*.pdf" })
            {
                if (dialog.ShowDialog() == DialogResult.OK)
                {
                    axAcroPDF1.src = dialog.FileName;
                    SplitPDFOnMemory(dialog.FileName);
                    TranslateButton.Enabled = true;
                }
            }
        }

        private void SplitPDFOnMemory(string fileName)
        {
            // Open the file
            PdfDocument inputDocument = PdfReader.Open(fileName, PdfDocumentOpenMode.Import);
            string name = Path.GetFileNameWithoutExtension(fileName);
            textBox2.Text = inputDocument.PageCount.ToString();
            _pageCount = inputDocument.PageCount;
            for (int idx = 0; idx < inputDocument.PageCount; idx++)
            {
                // Create new document
                PdfDocument outputDocument = new PdfDocument();
                outputDocument.Version = inputDocument.Version;
                outputDocument.Info.Title =
                String.Format("Page {0} of {1}", idx + 1, inputDocument.Info.Title);
                outputDocument.Info.Creator = inputDocument.Info.Creator;
                // Add the page and save it
                outputDocument.AddPage(inputDocument.Pages[idx]);
                onePageDocumentList.Add(outputDocument);
                //outputDocument.Save(String.Format("{0} - Page {1}_tempfile.pdf", name, idx + 1));
             }
        }

        private int ValidateTextBox1()
        {
            int pageIndex = 0;
            if (int.TryParse(textBox1.Text, out pageIndex) == false)
                return -1;
            else
            { 
                if (pageIndex <= 0 || pageIndex > _pageCount)
                {
                    richTextBox1.Text = "";
                    return -1;
                }
                return pageIndex;
            }
        }

        private void TranslateButton_Click(object sender, EventArgs e)
        {
            //int pageIndex = ValidateTextBox1();
            //if (pageIndex != -1)
            //{
            //    ExtractAndTranslateByIndex(pageIndex - 1);
            //    axAcroPDF1.setCurrentPage(pageIndex);
            //}

            
            int pageIndex = ValidateTextBox1();
            if (pageIndex != -1)
            {
                pageIndex++;
                if (pageIndex <= _pageCount)
                {
                    ExtractAndTranslateByIndex(pageIndex - 1);
                    axAcroPDF1.setCurrentPage(pageIndex);
                    textBox1.Text = pageIndex.ToString();
                }
            }

        }

        private void ExtractAndTranslateByIndex(int pageIndex)
        {
            PdfDocument tempDoc = onePageDocumentList[pageIndex];
            Stream stream = new MemoryStream();
            tempDoc.Save(stream, false);
            PdfExtract.Extractor extractor = new PdfExtract.Extractor();
            string temp = "";
            string temp1 = "";
            temp1 = extractor.ExtractToString(stream, Encoding.UTF8);

            temp = ReplaceSpecialKeyBeforeTranslate(temp1);
            string translatedTemp = TranslateWithGoogle.Translate(temp, "auto", "ko");
            translatedTemp = ReplaceSpecialKeyAfterTranslate(translatedTemp);
            richTextBox1.Text = translatedTemp;
            totalString += richTextBox1.Text;
        }

        private string ReplaceSpecialKeyBeforeTranslate(string originText)
        {
            string value = "";
            value = originText.Replace("\r\n", "!!!!");// 'Carriage-Return-Linefeed
            value = value.Replace("\r", "!!!!"); //'Carriage Return
            value = value.Replace("\n", "!!!!");// 'Linefeed
            //value = value.Replace("\"", "%22");
            //value = value.Replace("&", "%26");
            //value = value.Replace("@", "%40");
            //value = value.Replace("#", "%23");
            //value = value.Replace("$", "%24");
            //value = value.Replace("=", "%3D");
            //value = value.Replace("+", "%2B");
            //value = value.Replace(";", "%3B");
            //value = value.Replace(":", "%3A");
            //value = value.Replace(",", "%2C");
            //value = value.Replace("/", "%2F");
            //value = value.Replace("$", "%24");
            //value = value.Replace("?", "%3F");
            return value;
        }

        private string ReplaceSpecialKeyAfterTranslate(string originText)
        {
            string value = "";
            value = originText.Replace("!!!!", "\r\n\r\n");// 'Carriage-Return-Linefeed
            value = value.Replace("&quot;", "\"");
            //value = value.Replace("% 26", "&");
            //value = value.Replace("% 40", "@");
            //value = value.Replace("% 23", "#");
            //value = value.Replace("% 24", "$");
            //value = value.Replace("% 3D", "=");
            //value = value.Replace("% 2B", "+");
            //value = value.Replace("% 3B", ";");
            //value = value.Replace("% 3A", ":");
            //value = value.Replace("% 2C", ",");
            //value = value.Replace("% 2F", "/");
            //value = value.Replace("% 24", "$");
            //value = value.Replace("% 3F", "?");
            //value = value.Replace("% 22", "\"");
            return value;
        }

        private void textBox1_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.KeyData == Keys.Enter)
            {
                int pageIndex = ValidateTextBox1();
                if (pageIndex != -1)
                {
                    ExtractAndTranslateByIndex(pageIndex - 1);
                    axAcroPDF1.setCurrentPage(pageIndex);
                }
            }
        }

        private void textBox3_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.KeyData == Keys.Enter)
            {
                int fontSize = 14;

                if (int.TryParse(FontSizeBox.Text, out fontSize))
                {
                    richTextBox1.Font = new Font(FontFamily.GenericSansSerif, fontSize);
                }
            }
        }

        private void button1_Click(object sender, EventArgs e)
        {
            // Open the file
            PdfDocument inputDocument = PdfReader.Open(axAcroPDF1.src, PdfDocumentOpenMode.Import);
            string name = Path.GetFileNameWithoutExtension(axAcroPDF1.src);
            PdfExtract.Extractor extractor = new PdfExtract.Extractor();
            string temp1 = "";
            PdfDocument tempDoc = inputDocument;
            Stream stream = new MemoryStream();
            tempDoc.Save(stream, false);
            temp1 = extractor.ExtractToString(stream, Encoding.UTF8);


            FileStream fileStream = new FileStream(axAcroPDF1.src + ".text", FileMode.Create, FileAccess.Write);
            StreamWriter streamWriter = new StreamWriter(fileStream, Encoding.UTF8);
            streamWriter.Write(extractor.ExtractToString(stream, Encoding.UTF8));

            
        }


        //private void ExtractAndTranslatePDF(string fileName)
        //{
        //    PdfExtract.Extractor extractor = new PdfExtract.Extractor();
        //    Stream stream = new FileStream(fileName, FileMode.Open);
        //    textBox1.Text = extractor.ExtractToString(stream, Encoding.UTF8);

        //    int TextLen = textBox1.Text.Length;
        //    for (int i = 0; i < TextLen / 3000 + 1; i++)
        //    {
        //        string temp = "";
        //        if (i * 4000 + 4000 > TextLen)
        //            temp = textBox1.Text.Substring(i * 4000);
        //        else
        //            temp = textBox1.Text.Substring(i * 4000, 4000);


        //        textBox2.Text += TranslateWithGoogle.Translate(temp, "auto", "ko");
        //    }

        //    //XPdfForm xPdfForm = XPdfForm.FromFile(fileName);
        //    //XpdfNet.XpdfHelper helper = new XpdfNet.XpdfHelper();

        //    //textBox1.Text = helper.ToText(fileName);


        //    //_document = PdfReader.Open(fileName);
        //    //foreach (PdfPage page in _document.Pages)
        //    //{
        //    //    IEnumerable<string> bb;
        //    //    bb = page.ExtractText();
        //    //    ICollection<string> cc = page.Elements.Keys;
        //    //    ICollection<PdfItem> ct = page.Elements.Values;
        //    //    bb = page.ExtractText();
        //    //    string temp = "";
        //    //    foreach (var str in bb.ToList())
        //    //    {
        //    //        temp += str;
        //    //    }

        //    //    textBox1.Text += TranslateWithGoogle.Translate(temp, "auto", "ko");
        //    //}
        //}


    }
}
