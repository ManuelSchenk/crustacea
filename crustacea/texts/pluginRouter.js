/*
* This file containes the routes which where triggered from the client (frontend) who:
* - deploy dynamic endpoints for the communication between the:
*     - webhook for the external python plugin microservices (POST)
*     - polling from pisa client/frontend (GET)
* - starts the external python plugin microservices request
*/

import express from 'express';
export var router = express.Router();
router.use(express.json());
import { Request, Response } from 'express';

import FormData from 'form-data';
import multer from 'multer';
import { getGroundFovParameter } from '../services/pluginsParameterService';
import { callPlugin } from '../utils/pluginRouterUtils';

export interface generalParameters {
  variantName: string;
  nrcsIteration: number;
  project: number;
  variantId: number;
}

const upload = multer();

router.post('/dummy_post_webhook_endpoint', (req, res) => {
  console.log("POST request on dummy_post_webhook_endpoint received.");
  res.sendStatus(200); // Sends headers without a body
}
);

router.post('/form/cis/groundFOV',
  wrapHandler(async (req) => {
    const serviceUrl = 'http://pisa_plugin_groundFov:2001/start';

    // collect basic parameter form pisa db
    const generalParameters: generalParameters = req.body.generalParameters
    const groundFovData = await getGroundFovParameter(generalParameters.variantId, generalParameters.nrcsIteration)

    const { pluginResponse, jobId } = await callPlugin(serviceUrl, groundFovData);
    return { jobId, pluginResponse }
  }
  ));


router.post('/drop/dynamicMasking',
  upload.single('image'),
  wrapHandler(async (req) => {
    const serviceUrl = 'http://pisa_plugin_dynamic_masking:2003/start';



    if (req.file) {
      const formData = new FormData();
      // Append the file as `file_content` with proper filename and content type
      formData.append('file_content', req.file.buffer, {
        filename: req.file.originalname,
        contentType: req.file.mimetype
      });

      const { pluginResponse, jobId } = await callPlugin(serviceUrl, formData);
      // pluginResponse containes a status code 202 and the webhook url for the client
      return { jobId, pluginResponse };
    } else {
      console.error('Request on /drop/dynamicMasking did not contain an image');
      throw new Error('Invalid request. No image file found.');
    }
  }
  ));

export function wrapHandler(handler: (req: Request) => Promise<any>) {
  return async (req: Request, res: Response) => {
    try {
      const { jobId, pluginResponse } = await handler(req);
      res.status(202).send({  // this is the respond to the frontend with webhookURL for status polling
        message: 'Process started, send cookie UUID.',
        data: {
          job_id: jobId,
          plugin_response: pluginResponse,
          // the webhook url for the client/frontend dont need the full URL because it proxies all requests to the backend automatically
          webhook_url: `/dynamic/${jobId}`,  // so no ip or domain name is needed here!
        },
      });
    } catch (error: any) {
      console.error('Error in plugin route handler:', error.message);
      res.status(500).send({
        message: 'Failed to start process',
        error: error.message,
      });
    }
  };
}

export default router;
