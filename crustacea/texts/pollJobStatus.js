import axios from 'axios';

// Define the job state types
export type PythonState = 'Created' | 'Pending' | 'In Progress' | 'Finished' | 'Failed';
// Define the PluginJob class as you specified
export class PluginJob {
    id: string;
    progress: number;
    state: PythonState;
}

// Define the return type for better TypeScript support
export interface PollerControls {
    stop: () => void;
}

/**
 * Polling function that checks status of the plugin jobs and runs a callback on progress, finished or error
 * @param {string} jobId - The ID of the job to poll
 * @param {string} webhookUrl - The webhook URL to poll
 * @param {Function} onFinished - Callback when job is finished (receives jobId)
 * @param {Function} onProgress - Optional callback for job progress updates
 * @param {Function} onError - Optional callback for error handling
 * @returns {Object} Control object with stop method
 */
export const pollJobStatus = (
    jobId: string,
    webhookUrl: string,
    onFinished: (job: PluginJob) => void = () => { },
    onProgress: (job: PluginJob) => void = () => { },
    onError: (error: Error) => void = () => { }
): PollerControls => {
    const pollingInterval = 1000;
    const maxRetries = 5;
    let retryCount = 0;

    // Start polling at regular intervals
    const intervalId = setInterval(async () => {
        try {
            // Axios GET will throw if status is not 2xx
            const response = await axios.get(webhookUrl);

            // Reset retry counter on a successful request
            retryCount = 0;
            const job: PluginJob = response.data;
            onProgress(job);

            // Check if job is finished
            if (job.state === 'Finished') {
                console.log(`Job ${jobId} finished processing`);
                clearInterval(intervalId);
                onFinished(job);
            }
        } catch (error) {
            retryCount++;
            console.error('Error fetching job status:', error);

            if (retryCount >= maxRetries) {
                console.error(`Max retries (${maxRetries}) reached. Stopping poll.`);
                clearInterval(intervalId);
                onError(error instanceof Error ? error : new Error(String(error)));
            }
        }
    }, pollingInterval);

    // Return object with methods to control polling
    return {
        // Method to stop polling
        stop: () => {
            clearInterval(intervalId);
        }
    };
};