select `order`.`Order ID`,Segment,`Order Priority`,Market,sum(`Shipping Cost`) as Shipping_cost_avg,MAX(case when Category = 'Furniture' then 1 else 0 end)
as Category_Furniture,MAX(case when Category = 'Office Supplies' then 1 else 0 end) as Category_officeSup,Max(case when Category = 'Technology' then 1 else 0 end)
as Category_Technology ,City,State,Country,Region from order_detail join`order` on order_detail.`Order ID` = `order`.`Order ID` join customer on
`order`.`Customer ID` = customer.`Customer ID` join product on product.`Product ID` = order_detail.`Product ID` join shipping
on `order`.`Order ID` = shipping.`Order ID` group by `Order ID`,Segment,`Order Priority`,Market,City,State,Country,Region