using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading.Tasks;

namespace PDFTranslateInDesktop
{
    class TranslateWithGoogle
    {
        /// <summary>
        /// Translate Text without using Google Translate API's
        //string translation = Translate("Your text to translate.", "en", "tr");

        public static string Translate(string text, string from, string to)
        {
            string page = null;
            try
            {
                WebClient wc = new WebClient();
                wc.Headers.Add(HttpRequestHeader.UserAgent, "Mozilla/5.0");
                wc.Headers.Add(HttpRequestHeader.AcceptCharset, "UTF-8");
                wc.Encoding = Encoding.UTF8;

                string url = string.Format(@"http://translate.google.com.tr/m?hl=ko&sl={0}&tl={1}&ie=UTF-8&prev=_m&q={2}",
                                            from, to, Uri.EscapeUriString(text));

                page = wc.DownloadString(url);
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.ToString());
                return null;
            }

            page = page.Remove(0, page.IndexOf("<div dir=\"ltr\" class=\"t0\">")).Replace("<div dir=\"ltr\" class=\"t0\">", "");
            int last = page.IndexOf("</div>");
            page = page.Remove(last, page.Length - last);

            return page;
        }
    }
}
