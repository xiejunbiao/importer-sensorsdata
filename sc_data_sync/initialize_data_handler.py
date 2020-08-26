from .hisense_to_sqyn_sc_abstract import SynchronizeData


class InitDataHandler(SynchronizeData):

    def init_start(self):
        # tables_li = ['cb_sc_sale_order', 'cb_sc_sale_return_sku']
        tables_li = ['cb_sc_sale_return_sku']
        for table in tables_li:
            self.initialize_table(table)
        self.hisense_conn.close()
        self.sqyn_sc_conn.close()

    def initialize_table(self, table):
        if table == 'cb_sc_sale_order':
            select_sql = '''SELECT
                s_order.bill_no, 
                s_order.bill_status, 
                s_order.owner_code, 
                s_order.owner_name, 
                s_order.should_pay_total, 
                s_order.discount_total, 
                s_order.delivery_total, 
                s_order.real_pay_total, 
                s_order.count, 
                s_order.rec_code, 
                s_order.rec_area_code, 
                s_order.rec_name, 
                s_order.rec_address, 
                s_order.rec_phone, 
                s_order.created_time, 
                s_order.pay_click_time, 
                s_order.paid_time, 
                s_order.used_store_no, 
                s_order.is_point_used, 
                s_order.used_point_no, 
                s_order.used_point, 
                s_order.income_point_no, 
                s_order.income_point, 
                s_order.pay_type, 
                s_order.unipay_bill_no, 
                s_order.cancelled_time, 
                s_order.remark, 
                s_order.coupon_code, 
                s_order.coupon_total, 
                s_order.delivery_type, 
                s_order.pickup_name, 
                s_order.pickup_phone, 
                s_order.bill_type, 
                s_order.area_code, 
                s_order.room_code, 
                s_order.room_full_name, 
                s_order.nostore_choice, 
                s_order.act_total, 
                s_order.pack_total, 
                s_area.AREA_NAME 
            FROM
                sale_order AS s_order
                INNER JOIN t_code_sync_area AS s_area ON s_order.area_code = s_area.AREA_CODE
            WHERE
                TO_DAYS(paid_time) <= TO_DAYS('2020-06-29')
            LIMIT %s, %s'''
            insert_sql = '''insert into {}(
                bill_no, 
                bill_status, 
                owner_code, 
                owner_name, 
                should_pay_total, 
                discount_total, 
                delivery_total, 
                real_pay_total, 
                spu_count, 
                rec_code, 
                rec_area_code, 
                rec_name, 
                rec_address, 
                rec_phone, 
                created_time, 
                pay_click_time, 
                paid_time, 
                used_store_no, 
                is_point_used, 
                used_point_no, 
                used_point, 
                income_point_no, 
                income_point, 
                pay_type, 
                unipay_bill_no, 
                cancelled_time, 
                remark, 
                coupon_code, 
                coupon_total, 
                delivery_type, 
                pickup_name, 
                pickup_phone, 
                bill_type, 
                area_code, 
                room_code, 
                room_full_name, 
                nostore_choice, 
                act_total, 
                pack_total, 
                area_name                 
            )
            values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
                bill_status = VALUES(bill_status),
                owner_code = VALUES(owner_code),
                owner_name = VALUES(owner_name),
                should_pay_total = VALUES(should_pay_total),
                discount_total = VALUES(discount_total),
                delivery_total = VALUES(delivery_total),
                real_pay_total = VALUES(real_pay_total),
                spu_count = VALUES(spu_count),
                rec_code = VALUES(rec_code),
                rec_area_code = VALUES(rec_area_code),
                rec_name = VALUES(rec_name),
                rec_address = VALUES(rec_address),
                rec_phone = VALUES(rec_phone),
                created_time = VALUES(created_time),
                pay_click_time = VALUES(pay_click_time),
                paid_time = VALUES(paid_time),
                used_store_no = VALUES(used_store_no),
                is_point_used = VALUES(is_point_used),
                used_point_no = VALUES(used_point_no),
                used_point = VALUES(used_point),
                income_point_no = VALUES(income_point_no),
                income_point = VALUES(income_point),
                pay_type = VALUES(pay_type),
                unipay_bill_no = VALUES(unipay_bill_no),
                cancelled_time = VALUES(cancelled_time),
                remark = VALUES(remark),
                coupon_code = VALUES(coupon_code),
                coupon_total = VALUES(coupon_total),
                delivery_type = VALUES(delivery_type),
                pickup_name = VALUES(pickup_name),
                pickup_phone = VALUES(pickup_phone),
                bill_type = VALUES(bill_type),
                area_code = VALUES(area_code),
                room_code = VALUES(room_code),
                room_full_name = VALUES(room_full_name),
                nostore_choice = VALUES(nostore_choice),
                pack_total = VALUES(pack_total),
                act_total = VALUES(act_total),
                area_name = VALUES(area_name)
            '''.format(table)
        else:
            select_sql = '''SELECT
                r_sku.bill_no, 
                r_sku.sku_no, 
                r_sku.sale_order_bill_no, 
                r_sku.sale_order_sub_bill_no, 
                r_sku.bill_status, 
                r_sku.first_audit, 
                r_sku.second_audit, 
                r_sku.owner_code, 
                r_sku.owner_name, 
                r_sku.area_code, 
                r_sku.shop_code, 
                r_sku.shop_name, 
                r_sku.spu_code, 
                r_sku.spu_name, 
                r_sku.attr_value_content, 
                r_sku.sku_price, 
                r_sku.return_reason, 
                r_sku.return_count, 
                r_sku.return_real_total, 
                r_sku.delivery_total, 
                r_sku.return_address, 
                r_sku.sku_pic_url, 
                r_sku.return_total, 
                r_sku.unionpay_refund_no, 
                r_sku.return_time, 
                r_sku.used_reverse_point, 
                r_sku.income_reverse_point, 
                r_sku.created_time, 
                r_sku.updated_time, 
                r_sku.remark, 
                r_sku.real_return_count, 
                r_sku.created_user, 
                r_sku.updated_user, 
                r_sku.audit_time, 
                r_sku.pack_total, 
                r_sku.covering_letter, 
                s_order.area_code, 
                s_area.AREA_NAME
            FROM
                sale_return_sku AS r_sku
                INNER JOIN sale_order as s_order ON r_sku.sale_order_bill_no = s_order.bill_no
                INNER JOIN t_code_sync_area AS s_area ON s_order.area_code = s_area.AREA_CODE
            WHERE
                TO_DAYS(return_time) <= TO_DAYS('2020-06-29')
            LIMIT %s, %s'''
            insert_sql = '''insert into {}(
                bill_no_return, 
                sku_no, 
                bill_no, 
                sub_bill_no, 
                bill_status_return, 
                first_audit, 
                second_audit, 
                owner_code, 
                owner_name, 
                area_code, 
                shop_code, 
                shop_name, 
                spu_code, 
                spu_name, 
                attr_value_content, 
                sku_price, 
                return_reason, 
                return_count, 
                return_real_total, 
                delivery_total_return, 
                return_address, 
                sku_pic_url, 
                return_total, 
                unionpay_refund_no, 
                return_time, 
                used_reverse_point, 
                income_reverse_point, 
                created_time, 
                updated_time, 
                remark, 
                real_return_count, 
                created_user, 
                updated_user, 
                audit_time, 
                pack_total, 
                covering_letter, 
                order_area_code, 
                order_area_name
            )
            values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
                sku_no = VALUES(sku_no),
                bill_no = VALUES(bill_no),
                sub_bill_no = VALUES(sub_bill_no),
                bill_status_return = VALUES(bill_status_return),
                first_audit = VALUES(first_audit),
                second_audit = VALUES(second_audit),
                owner_code = VALUES(owner_code),
                owner_name = VALUES(owner_name),
                area_code = VALUES(area_code),
                shop_code = VALUES(shop_code),
                shop_name = VALUES(shop_name),
                spu_code = VALUES(spu_code),
                spu_name = VALUES(spu_name),
                attr_value_content = VALUES(attr_value_content),
                sku_price = VALUES(sku_price),
                return_reason = VALUES(return_reason),
                return_count = VALUES(return_count),
                return_real_total = VALUES(return_real_total),
                delivery_total_return = VALUES(delivery_total_return),
                return_address = VALUES(return_address),
                sku_pic_url = VALUES(sku_pic_url),
                return_total = VALUES(return_total),
                unionpay_refund_no = VALUES(unionpay_refund_no),
                return_time = VALUES(return_time),
                used_reverse_point = VALUES(used_reverse_point),
                income_reverse_point = VALUES(income_reverse_point),
                created_time = VALUES(created_time),
                updated_time = VALUES(updated_time),
                remark = VALUES(Remark),
                real_return_count = VALUES(real_return_count),
                created_user = VALUES(created_user),
                updated_user = VALUES(updated_user),
                audit_time = VALUES(audit_time),
                pack_total = VALUES(pack_total),
                covering_letter = VALUES(covering_letter),
                order_area_code = VALUES(order_area_code),
                order_area_name = VALUES(order_area_name)
            '''.format(table)
        self.mysql_operation(select_sql, insert_sql, table)


if __name__ == '__main__':
    pass
    # idh = InitDataHandler()