import React, { useState, useEffect, useRef } from "react";
import Dropzone from "../../common/Dropzone";
import ProgressSpinner from "../../common/ProgressSpinner";
import { pollJobStatus, PollerControls, PluginJob } from "../../../utils/pollJobStatus";
import styles from "./DynamicMaskingPage.module.css";

const DynamicMaskingPage = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [imageSrc, setImageSrc] = useState(null); // State to store the Base64 image source
  const [dropzoneImage, setDropzoneImage] = useState(null); // Uploaded image from Dropzone
  const [jobProgress, setJobProgress] = useState(0);
  const [jobState, setJobState] = useState(null);
  const [errorMessage, setErrorMessage] = useState < string > "";

  // Reference to store the poller for cleanup
  const pollerRef = (useRef < PollerControls) | (null > null);

  // Clean up function to abort any ongoing requests when component unmounts
  useEffect(() => {
    const controller = new AbortController();
    return () => {
      controller.abort();
      // Stop any active polling
      if (pollerRef.current) {
        pollerRef.current.stop();
      }
    };
  }, []);

  // Example usage in your component
  const handleFileSubmit = async (fileInput) => {
    console.log("Files for upload (only the first image will be processed):", fileInput);
    setIsLoading(true);
    setJobProgress(0);
    setJobState("Created");
    setErrorMessage("");
    setImageSrc(null); // Reset the image source before uploading a new file

    // Normalize file input handling
    let files;
    if (Array.isArray(fileInput)) {
      files = Array.isArray(fileInput[0]) ? fileInput[0] : fileInput;
    } else {
      files = [fileInput];
    }

    // Check if we have valid files
    if (!(files.length > 0 && files[0] instanceof File)) {
      console.error("Invalid file object:", files[0]);
      setIsLoading(false);
      setErrorMessage("Failed to upload file. Please try again.");
      return;
    }

    // Set the preview image
    const file = files[0]; // we took only the first file but we reuse the interface
    const reader = new FileReader();
    reader.onload = (e) => setDropzoneImage(e.target.result);
    // this sets up a callback that will update the dropzoneImage with the file's contents
    // as a Base64-encoded data URL once the file is fully loaded
    reader.readAsDataURL(file);
    // this starts reading in the content from "file" as a data URL (=Base64 encoded)

    // Build and send the FormData
    const formData = new FormData();
    formData.append("image", file);

    try {
      const response = await fetch("/drop/dynamicMasking", {
        method: "POST",
        body: formData,
      });
      if (!response.ok) {
        const errorData = await response.json();
        console.error("FastAPI Error:", errorData);
        setIsLoading(false);
        return;
      }

      // Start polling from GET webhook for the job state with callbacks
      pollerRef.current = pollJobStatus(
        jobId,
        webhookUrl,

        // onFinished callback
        async (job: PluginJob) => {
          try {
            const dynamicMask = await fetch(`/getDynamicMaskingResultImage?jobId=${job.id}`);

            if (dynamicMask.ok) {
              const result = await dynamicMask.json();
              setImageSrc(result.b64Image);
            } else {
              // Simple error handling - just use the status info
              const errorText = await dynamicMask.text();
              const errorMessage = `Request failed with status: ${dynamicMask.status} ${dynamicMask.statusText}\n ${errorText})`;
              console.error(errorMessage);
              setErrorMessage(errorMessage);
            }
          } catch (error) {
            console.error("Error fetching the result image:", error);
            setErrorMessage(`Network error: ${error.message}`);
          } finally {
            setIsLoading(false);
          }
        },

        // onProgress callback
        (job: PluginJob) => {
          setJobProgress(job.progress);
          setJobState(job.state);
          console.log(`Polling Job ${job.id} progress: ${job.progress}%, state: ${job.state}`);
        },

        // onError callback
        (error) => {
          console.error("Polling error:", error);
          setIsLoading(false);
          setErrorMessage(`Error polling job status: ${error.message}`);
        }
      );
    } catch (error) {
      console.error("Error uploading files:", error);
      setIsLoading(false);
      setErrorMessage("An unexpected error occurred while uploading.");
    }
  };

  return True;
};
export default DynamicMaskingPage;
