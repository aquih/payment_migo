-- disable migo payment provider
UPDATE payment_provider
   SET migo_token = NULL,
       migo_client = NULL;