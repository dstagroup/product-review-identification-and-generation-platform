import re
import subprocess
from amazon_buddy import Product, AmazonBuddy, Category, SortType

class AmazonCrawler:
    """
    This is a class for Amazon crawling
    """
    def __init__(self):
        """
        Init crawling
        """
        self.ab = AmazonBuddy(debug=True, user_agent='ADD_USER_AGENT')

    def SetUrl(self,url,reviewNum=200,minRating=0.0,maxRating=5.0,debug=False):
        """
        According url to get asin num to get review
        """
        if debug==False:
            if url==None:
                raise NameError("Undefined url") from Exception
            if reviewNum<100 or reviewNum>=10000:
                raise ValueError("The number of comments is between 100 and 10000") from Exception
            if minRating<0.0 or minRating>5.0:
                raise ValueError("The value of minimum rating is between 0.0 and 5.0") from Exception
            if maxRating<0.0 or maxRating>5.0:
                raise ValueError("The value of maximum rating is between 0.0 and 5.0") from Exception
        asinRegularFormula="dp/[\w]*/ref"
        try:
            asin=re.search(asinRegularFormula,url).group().split("/")[1]

        except:
            raise AttributeError("Can't find asin,please check the url.") from Exception
        sentence="amazon-buddy reviews {} -n {} --min-rating {} --max-rating {}".format(asin,reviewNum,minRating,maxRating)
        storefileName=subprocess.getoutput(sentence).split(":")[1].split(" ")
        return storefileName


a=AmazonCrawler()
a.SetUrl("https://www.amazon.com/dp/B01GW3H3U8/ref=sspa_dk_detail_1?psc=1&pd_rd_i=B09XML1K5Z&pd_rd_w=keJQr&content-id=amzn1.sym.56b6d1e1-8781-4e32-a7bc-5298ad4b88ac&pf_rd_p=56b6d1e1-8781-4e32-a7bc-5298ad4b88ac&pf_rd_r=8EQRDV8898SFVBQS6P45&pd_rd_wg=4ocBb&pd_rd_r=7f2299ed-2353-4777-b813-9d3cb941f188&s=kitchen&sp_csd=d2lkZ2V0TmFtZT1zcF9kZXRhaWwy&smid=A6JZUY2ZWGBG5&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEzMFVCUjZIWklLQTJJJmVuY3J5cHRlZElkPUEwMTEwMDczQk1UVlUyRTk3UFNNJmVuY3J5cHRlZEFkSWQ9QTAyOTQ5OTgzTzRUTTUwRlRWUEhOJndpZGdldE5hbWU9c3BfZGV0YWlsMiZhY3Rpb249Y2xpY2tSZWRpcmVjdCZkb05vdExvZ0NsaWNrPXRydWU=",200,0.0,5.0,False)

