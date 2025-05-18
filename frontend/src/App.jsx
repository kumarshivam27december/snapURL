// import { useState, useEffect } from 'react'
// import {
//   Box,
//   VStack,
//   Heading,
//   Input,
//   Button,
//   Text,
//   Image,
//   SimpleGrid,
//   Container,
//   Link,
//   Icon,
//   useToast,
// } from '@chakra-ui/react'
// import { FiUpload, FiLink } from 'react-icons/fi'
// import axios from 'axios'

// const API_URL = 'https://snapurl-xrth.onrender.com/api'

// function App() {
//   const [selectedFile, setSelectedFile] = useState(null)
//   const [uploadedImages, setUploadedImages] = useState([])
//   const [isLoading, setIsLoading] = useState(false)
//   const toast = useToast()

//   useEffect(() => {
//     fetchImages()
//   }, [])

//   const fetchImages = async () => {
//     try {
//       const response = await axios.get(`${API_URL}/images`)
//       setUploadedImages(response.data)
//     } catch (error) {
//       console.error('Error fetching images:', error)
//       toast({
//         title: 'Error fetching images',
//         description: error.message,
//         status: 'error',
//         duration: 3000,
//         isClosable: true,
//       })
//     }
//   }

//   const handleFileSelect = (event) => {
//     setSelectedFile(event.target.files[0])
//   }

//   const handleUpload = async () => {
//     if (!selectedFile) {
//       toast({
//         title: 'No file selected',
//         description: 'Please select an image to upload',
//         status: 'warning',
//         duration: 3000,
//         isClosable: true,
//       })
//       return
//     }

//     setIsLoading(true)
//     const formData = new FormData()
//     formData.append('file', selectedFile)

//     try {
//       const response = await axios.post(`${API_URL}/upload`, formData, {
//         headers: {
//           'Content-Type': 'multipart/form-data',
//         },
//       })
//       toast({
//         title: 'Upload successful',
//         description: 'Your image has been uploaded',
//         status: 'success',
//         duration: 3000,
//         isClosable: true,
//       })
//       setSelectedFile(null)
//       fetchImages()
//     } catch (error) {
//       console.error('Upload error:', error)
//       toast({
//         title: 'Upload failed',
//         description: error.response?.data?.detail || error.message,
//         status: 'error',
//         duration: 3000,
//         isClosable: true,
//       })
//     } finally {
//       setIsLoading(false)
//     }
//   }

//   return (
//     <Container maxW="container.xl" py={8}>
//       <VStack spacing={8}>
//         <Heading>SnapURL - Image Hosting</Heading>
        
//         <Box w="full" p={6} borderWidth={1} borderRadius="lg" boxShadow="lg">
//           <VStack spacing={4}>
//             <Input
//               type="file"
//               accept="image/*"
//               onChange={handleFileSelect}
//               display="none"
//               id="file-upload"
//             />
//             <Button
//               as="label"
//               htmlFor="file-upload"
//               leftIcon={<Icon as={FiUpload} />}
//               colorScheme="blue"
//               cursor="pointer"
//             >
//               Select Image
//             </Button>
//             {selectedFile && (
//               <Text>Selected: {selectedFile.name}</Text>
//             )}
//             <Button
//               onClick={handleUpload}
//               isLoading={isLoading}
//               colorScheme="green"
//               leftIcon={<Icon as={FiLink} />}
//             >
//               Upload & Get URL
//             </Button>
//           </VStack>
//         </Box>

//         <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={6} w="full">
//           {uploadedImages.map((image, index) => (
//             <Box
//               key={index}
//               borderWidth={1}
//               borderRadius="lg"
//               overflow="hidden"
//               boxShadow="md"
//             >
//               <Image
//                 src={image.url}
//                 alt={image.original_filename}
//                 objectFit="cover"
//                 h="200px"
//                 w="full"
//               />
//               <Box p={4}>
//                 <Text fontSize="sm" color="gray.500">
//                   {new Date(image.uploaded_at).toLocaleString()}
//                 </Text>
//                 <Link href={image.url} isExternal color="blue.500">
//                   {image.url}
//                 </Link>
//               </Box>
//             </Box>
//           ))}
//         </SimpleGrid>
//       </VStack>
//     </Container>
//   )
// }

// export default App
import { useState, useEffect } from 'react'
import {
  Box,
  VStack,
  Heading,
  Input,
  Button,
  Text,
  Image,
  SimpleGrid,
  Container,
  Link,
  Icon,
  useToast,
} from '@chakra-ui/react'
import { FiUpload, FiLink } from 'react-icons/fi'
import axios from 'axios'

const API_URL = 'https://snapurl-xrth.onrender.com/api'

function App() {
  const [selectedFile, setSelectedFile] = useState(null)
  const [uploadedImages, setUploadedImages] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const toast = useToast()

  useEffect(() => {
    fetchImages()
  }, [])

  const fetchImages = async () => {
    try {
      const response = await axios.get(`${API_URL}/images`)
      setUploadedImages(response.data)
    } catch (error) {
      console.error('Error fetching images:', error)
      toast({
        title: 'Error fetching images',
        description: error.message,
        status: 'error',
        duration: 3000,
        isClosable: true,
      })
    }
  }

  const handleFileSelect = (event) => {
    setSelectedFile(event.target.files[0])
  }

  const handleUpload = async () => {
    if (!selectedFile) {
      toast({
        title: 'No file selected',
        description: 'Please select an image to upload',
        status: 'warning',
        duration: 3000,
        isClosable: true,
      })
      return
    }

    setIsLoading(true)
    const formData = new FormData()
    formData.append('file', selectedFile)

    try {
      const response = await axios.post(`${API_URL}/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      toast({
        title: 'Upload successful',
        description: 'Your image has been uploaded',
        status: 'success',
        duration: 3000,
        isClosable: true,
      })
      setSelectedFile(null)
      fetchImages()
    } catch (error) {
      console.error('Upload error:', error)
      toast({
        title: 'Upload failed',
        description: error.response?.data?.detail || error.message,
        status: 'error',
        duration: 3000,
        isClosable: true,
      })
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Box
      minHeight="100vh"
      bgGradient="linear(to-r, gray.700, red.500, yellow.400, green.300, pink.300, blue.300)"
      backgroundSize="600% 600%"
      animation="gradientAnimation 20s ease infinite"
      p={0}
      m={0}
    >
      <style>
        {`
          @keyframes gradientAnimation {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
          }
        `}
      </style>

      <Container maxW="container.xl" py={8}>
        <VStack spacing={8}>
          <Heading color="white" textShadow="1px 1px 4px black">
            SnapURL - Image Hosting
          </Heading>

          <Box
            w="full"
            p={6}
            borderWidth={1}
            borderRadius="lg"
            boxShadow="lg"
            bg="whiteAlpha.200"
            backdropFilter="blur(10px)"
          >
            <VStack spacing={4}>
              <Input
                type="file"
                accept="image/*"
                onChange={handleFileSelect}
                display="none"
                id="file-upload"
              />
              <Button
                as="label"
                htmlFor="file-upload"
                leftIcon={<Icon as={FiUpload} />}
                colorScheme="pink"
                cursor="pointer"
              >
                Select Image
              </Button>
              {selectedFile && <Text color="white">{selectedFile.name}</Text>}
              <Button
                onClick={handleUpload}
                isLoading={isLoading}
                colorScheme="green"
                leftIcon={<Icon as={FiLink} />}
              >
                Upload & Get URL
              </Button>
            </VStack>
          </Box>

          <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={6} w="full">
            {uploadedImages.map((image, index) => (
              <Box
                key={index}
                borderWidth={1}
                borderRadius="lg"
                overflow="hidden"
                boxShadow="md"
                bg="whiteAlpha.300"
                backdropFilter="blur(8px)"
              >
                <Image
                  src={image.url}
                  alt={image.original_filename}
                  objectFit="cover"
                  h="200px"
                  w="full"
                />
                <Box p={4}>
                  <Text fontSize="sm" color="gray.200">
                    {new Date(image.uploaded_at).toLocaleString()}
                  </Text>
                  <Link href={image.url} isExternal color="teal.200">
                    {image.url}
                  </Link>
                </Box>
              </Box>
            ))}
          </SimpleGrid>
        </VStack>
      </Container>
    </Box>
  )
}

export default App
