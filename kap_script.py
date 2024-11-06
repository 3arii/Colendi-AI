# from pykap.get_general_info import get_general_info

# print(get_general_info(tick='KCHOL'))


# from pykap.bist import BISTCompany
# comp = BISTCompany(ticker='KCHOL')

# comp.get_expected_disclosure_list(count=10)

# # report_type="operating report"
# # operating_report = comp.get_historical_disclosure_list(fromdate = "2020-05-21",
# #                                     todate="2021-05-21", 
# #                                     disclosure_type="FR",
# #                                     subject=report_type)

# report_type="financial report"
# financial_report = comp.get_historical_disclosure_list(fromdate = "2020-05-21",
#                                     todate="2021-05-21", 
#                                     disclosure_type="FR",
#                                     subject=report_type)

# comp.save_operating_review(output_dir='OperatingReviews')

# # print(operating_report)

from pykap.bist_company_list import bist_company_list
print(bist_company_list())