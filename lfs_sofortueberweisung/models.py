# global imports
import hashlib
from lxml import etree
from lxml.builder import E
import requests

# django imports
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

# lfs imports
from lfs.plugins import PaymentMethodProcessor
from lfs.plugins import PM_ORDER_IMMEDIATELY

import logging
logger = logging.getLogger(__name__)


class SofortUeberweisungPaymentMethodProcessor(PaymentMethodProcessor):
    """
    Provides payment processment with sofortueberweisung.de.
    """
    def process(self):
        res = self.get_pay_link()
        if not res:
            return {'accepted': False,
                    'message': _('It was not possibe to process your request. Error while communicating with Sofortueberweisung.')}

        return {
            "accepted": True,
            "next_url": res
        }

    def get_pay_link(self):
        """
        http://example.com/sofort/notification_url/17/760437dfe6eacb4bd8d58c7807a778d3/
        http://example.com/sofort/notification_url/-USER_VARIABLE_1-/-USER_VARIABLE_2-/
        """
        key = '%s-%s-%s' % (settings.SECRET_KEY, self.order.pk, self.order.price)
        security_hash = hashlib.md5(key).hexdigest()
        return "https://www.sofortueberweisung.de/payment/start?user_id=%s&project_id=%s&reason_1=Bestellnummer %s&amount=%s&currency=EUR&user_variable_1=%s&user_variable_2=%s" % \
               (settings.SOFORTUEBERWEISUNG_USERID, settings.SOFORTUEBERWEISUNG_PROJECT_ID, self.order.number, self.order.price, self.order.pk, security_hash)


        # current_site = Site.objects.get_current()
        #
        # key = '%s-%s-%s' % (settings.SECRET_KEY, self.order.pk, self.order.price)
        # security_hash = hashlib.md5(key).hexdigest()
        #
        # data = E.multipay(
        #         E.project_id(str(settings.SOFORTUEBERWEISUNG_PROJECT_ID)),
        #         E.amount(str(self.order.price)),
        #         E.currency_code('EUR'),
        #         E.reasons(
        #             E.reason('Bestellnummer %s' % self.order.number)
        #         ),
        #         E.notification_urls(
        #             E.notification_url('%s://%s%s' % (getattr(settings, 'LFS_SOFORTUEBERWEISUNG_PROTOCOL', 'http'),
        #                                               current_site.domain,
        #                                               reverse('lfs_sofortueberweisung_notification',
        #                                                       kwargs={'order_id': self.order.pk,
        #                                                               'security_hash': security_hash})))
        #         )
        # )
        #
        # stringdata = etree.tostring(data, xml_declaration=True, encoding='utf-8')
        # headers = {'content-type': 'application/xml',
        #            'accept': 'application/xml'}
        #
        # try:
        #     r = requests.post(getattr(settings, 'LFS_SOFORTUEBERWEISUNG_API_URL', 'https://api.sofort.com/api/xml'),
        #                       data=stringdata,
        #                       auth=(str(settings.SOFORTUEBERWEISUNG_USERID), str(settings.SOFORTUEBERWEISUNG_API_KEY)),
        #                       headers=headers,
        #                       timeout=5)
        # except requests.Timeout:
        #     return None
        #
        # root = etree.XML(r.text)
        # return root.xpath('//payment_url/text()')[0]

    def get_create_order_time(self):
        return PM_ORDER_IMMEDIATELY
