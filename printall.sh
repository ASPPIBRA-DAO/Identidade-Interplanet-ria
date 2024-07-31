#!/usr/bin/env sh

# report
weasyprint report/report.html report/report.pdf &

# invoice
weasyprint invoice/invoice.html invoice/invoice.pdf &

# book
weasyprint -s book/book-classical.css book/book.html book/book-classical.pdf &
weasyprint -s book/book.css book/book.html book/book.pdf &