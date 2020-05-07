//
//  ViewController+CameraControllerDelegate.swift
//  FishAI-Mobile
//
//  Created by Alvin H Lai on 2020-05-07.
//  Copyright © 2020 Alvin H Lai. All rights reserved.
//

import UIKit
import AVFoundation

var stillImageOutput: AVCapturePhotoOutput!
var didTakePhoto = false

extension ViewController: UIImagePickerControllerDelegate, UINavigationControllerDelegate, AVCapturePhotoCaptureDelegate{
    
    override func viewDidLoad() {
        super.viewDidLoad()
    }

    override func viewWillAppear(_ animated: Bool) {
        //tempImageView.isHidden = true;
        super.viewWillAppear(animated)
        
        captureSession = AVCaptureSession()
        captureSession?.sessionPreset = AVCaptureSession.Preset.hd4K3840x2160
        
        guard let backCamera = AVCaptureDevice.default(.builtInWideAngleCamera, for: AVMediaType.video, position: .back)
            else {
                print("Unable to access front Camera")
                return
        }
        
        do {
            let input = try AVCaptureDeviceInput(device: backCamera)
            stillImageOutput = AVCapturePhotoOutput()
            
            if captureSession.canAddInput(input) && captureSession.canAddOutput(stillImageOutput) {
                captureSession.addInput(input)
                captureSession.addOutput(stillImageOutput)
                setupLivePreview()
            }
        }
        catch let error  {
            print("Error Unable to initialize back camera:  \(error.localizedDescription)")
        }
    }
    
    
    func setupLivePreview(){
        previewVideoLayer = AVCaptureVideoPreviewLayer(session: captureSession)
        previewVideoLayer.videoGravity = .resizeAspect
        previewVideoLayer.connection?.videoOrientation = .portrait
        cameraView.layer.addSublayer(previewVideoLayer)
        
        DispatchQueue.global(qos: .userInitiated).async{
            self.captureSession.startRunning()
            
            DispatchQueue.main.async {
                self.previewVideoLayer.frame = self.cameraView.bounds
            }
        }
    }
        
    func photoOutput(_ output: AVCapturePhotoOutput, didFinishProcessingPhoto photo: AVCapturePhoto, error: Error?)
    {
        guard let imageData = photo.fileDataRepresentation()
            else{return}

        let imageOutput = UIImage(data: imageData)
        let newImage = UIImage(cgImage: (imageOutput?.cgImage!)!, scale: imageOutput!.scale, orientation: .leftMirrored)
        
        didTakePhoto = didTakePhoto ? false : true;
        
        if (didTakePhoto == true){
            tmpImage.isHidden = false;
            tmpImage.semanticContentAttribute = .forceRightToLeft
            tmpImage.image = newImage
            cameraView.isHidden = true
            
            classify(image: newImage)
        }
        else{
            tmpImage.isHidden = true;
            cameraView.isHidden = false
            captureSession?.startRunning()
        }
        self.view.bringSubviewToFront(takePhotoButton)
    }
    
    override func viewWillDisappear(_ animated:Bool){
        super.viewWillDisappear(animated)
        self.captureSession.stopRunning()
    }

    
}


