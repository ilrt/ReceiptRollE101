import receipt_roll.plots.overview as ro
import receipt_roll.plots.radar as rr
import receipt_roll.plots.business_terms as rb


def generate_plots(save_to_file=True):
    # (1) overview of payments
    ro.plt_total_by_terms(save=save_to_file, title='1. Total payments per term', x_label='Terms',
                          y_label='Total payments', is_long_title=False, file='1_terms_total.png')
    # (2) days in the terms
    ro.plt_days_by_term(save=save_to_file, title='2. Number of days per term', x_label="Terms", y_label="Days",
                        is_long_title=False, file='2_terms_days.png')

    # (3) Items of business
    ro.plt_business_by_term(save=save_to_file, title='3. Total number of items of business per term', x_label="Terms",
                            y_label="Number of items of business", is_long_title=False, file='3_business_by_term.png')

    # (4–7) Radar plots of business
    rr.plt_terms_business_radar(save=save_to_file, file_name='plt_terms_business_radar.png', fig_num=4)

    # (8) Transactions and value as % of year, shown monthly
    rb.plt_transactions_and_totals_by_month(save=save_to_file,
                                            title='8. Number of transactions and their total value, '
                                                  'per month,\nas a percentage of the total for the year',
                                            x_label="Months", y_label="Percentage of total", is_long_title=False,
                                            file='8_plt_transactions_and_totals_by_month.png')

    # (9–12) Transactions and value as % of term, shown weekly
    rb.plt_transactions_total_as_pc_of_term(save=save_to_file, x_label='Week', y_label='Percentage of term total',
                                            fig_no=9, is_long_title=False,
                                            title="{}. {}\n No. of transactions and total receipts, per week,\n"
                                                  "as percentage of the term total",
                                            file_name='{}_{}_plt_transactions_total_as_pc_of_term.png')

    # (13-14) Sheriff's returns for Michaelmas and Easter
    rb.plt_sheriff_total_by_week_pc(save=save_to_file, term_name='Michaelmas', fig_no=13, is_long_title=False,
                                    title="{}. Weekly value of receipts returned {}", x_label="Week",
                                    y_label="Percentage value of receipts",
                                    file_name='{}_plt_sheriff_total_by_week_{}.png')
    rb.plt_sheriff_total_by_week_pc(save=save_to_file, term_name='Easter', fig_no=14, is_long_title=False,
                                    title="{}. Weekly value of receipts returned {}", x_label="Week",
                                    y_label="Percentage value of receipts",
                                    file_name='{}_plt_sheriff_total_by_week_{}.png')

    ro.plt_source_term_heat_map(save=save_to_file, title='15. Source of payments per term',
                                x_label="Payments per term", y_label="Source", is_long_title=False,
                                file='15_total_payments_source_heatmap.png')


if __name__ == '__main__':
    generate_plots()
